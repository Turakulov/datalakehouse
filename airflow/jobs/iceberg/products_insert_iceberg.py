from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, current_timestamp
import json

from pyspark.sql.types import (
    IntegerType,
    StringType,
    StructType,
    StructField,
    FloatType,
    LongType,
)

kafka_servers = "kafka:9093"
topic = "products"
database = "dwh"
iceberg_table = "dwh.products"
checkpoint_location = "/home/iceberg/data/checkpoints"

spark = (
    SparkSession.builder.appName(f"insert_iceberg_{topic}")
    .config("spark.default.parallelism", "10")
    .getOrCreate()
)

stream = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", kafka_servers)
    .option("subscribe", topic)
    .option("startingOffsets", "earliest")
    .option("failOnDataLoss", False)
    .option("checkpointLocation", checkpoint_location)
    .load()
)


def get_kafka_message_schema(topic):
    # # Получить небольшой объем данных из Kafka в батчевом режиме
    # sample_df = (
    #     spark.read.format("kafka")
    #     .option("kafka.bootstrap.servers", kafka_servers)
    #     .option("subscribe", topic)
    #     .option("startingOffsets", "earliest")  # Прочитать данные с начала
    #     .load()
    #     .selectExpr("CAST(value AS STRING) as value")
    #     .limit(100)  # Ограничиваем данные до первых 10 записей
    # )
    #
    # # Автоматически определить схему из батчевых данных
    # sample_json_df = spark.read.json(sample_df.rdd.map(lambda row: row.value))
    # # Получить схему данных

    with open("/root/airflow/jobs/iceberg/metadata.json", "r") as handle:
        metadata = json.load(handle)

    data_dict = metadata["tables"][topic.capitalize()]["columns"]

    # Маппинг sdtype и computer_representation на PySpark типы
    def get_spark_type(field_info):
        if field_info["sdtype"] == "categorical":
            return StringType()
        elif field_info["sdtype"] == "numerical":
            # Учитываем computer_representation
            if field_info.get("computer_representation") == "Float":
                return FloatType()
            elif field_info.get("computer_representation") == "Int64":
                return IntegerType()
            else:
                raise ValueError(
                    f"Unsupported computer_representation: {field_info.get('computer_representation')}"
                )
        elif field_info["sdtype"] == "id":
            return LongType()
        else:
            raise ValueError(f"Unsupported sdtype: {field_info['sdtype']}")

    # Генерация StructType
    message_schema = StructType(
        [
            StructField(field_name, get_spark_type(field_info), True)
            for field_name, field_info in data_dict.items()
        ]
    )

    return message_schema


def generate_create_table_sql(schema, table_name) -> str:
    # Соответствие типов PySpark и Iceberg
    type_mapping = {
        "StringType()": "STRING",
        "IntegerType()": "INT",
        "LongType()": "BIGINT",
        "DoubleType()": "DOUBLE",
        "FloatType()": "FLOAT",
        "BooleanType()": "BOOLEAN",
        "TimestampType()": "TIMESTAMP",
        "DateType()": "DATE",
        "BinaryType()": "BINARY",
    }

    # Генерация списка колонок
    columns = []
    for field in schema.fields:
        field_type = type_mapping.get(str(field.dataType), "STRING")
        columns.append(f"{field.name} {field_type}")

    # Формируем запрос CREATE TABLE
    columns_sql = """
    DWH_kafka_key STRING,
    DWH_kafka_partition INT,
    DWH_kafka_offset LONG,
    DWH_kafka_timestamp TIMESTAMP,
    DWH_load_timestamp TIMESTAMP,
    """ + ",\n    ".join(
        columns
    )
    create_table_sql = f"""
    CREATE OR REPLACE TABLE {table_name} ({columns_sql}
    )
    USING iceberg
    PARTITIONED BY (day(DWH_kafka_timestamp))
    COMMENT 'Table description or task id'
    TBLPROPERTIES(
        'write.sort.order' = 'DWH_kafka_offset'
    );"""

    return create_table_sql


def ensure_iceberg_table_exists(table_name, message_schema, database):
    # try:
    #     # Попытка чтения из таблицы для проверки её существования
    #     # spark.sql(f"SELECT 1 FROM {table_name} LIMIT 1")
    # except:
    # Если таблицы нет, создаём её
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {database}")
    # spark.sql(f"DROP TABLE IF EXISTS {table_name} PURGE")

    print(f"Recreating Iceberg table: {table_name}")
    create_table_sql = generate_create_table_sql(message_schema, table_name)
    print(create_table_sql)
    spark.sql(create_table_sql)


message_schema = get_kafka_message_schema(topic=topic)
print(message_schema)
ensure_iceberg_table_exists(
    table_name=iceberg_table, message_schema=message_schema, database=database
)

# Select and deserialize data
df_deserialized = stream.select(
    col("key").cast("string").alias("DWH_kafka_key"),  # Msg key
    col("topic").alias("DWH_kafka_topic"),  # Topic
    col("partition").alias("DWH_kafka_partition"),  # Kafka partition
    col("offset").alias("DWH_kafka_offset"),  # Kafka offset
    col("timestamp").alias("DWH_kafka_timestamp"),  # Msg timestamp
    from_json(col("value").cast("string"), message_schema).alias(
        "json_value"
    ),  # JSON value
).select(
    "DWH_kafka_key",
    "DWH_kafka_partition",
    "DWH_kafka_offset",
    "DWH_kafka_timestamp",
    current_timestamp().alias("DWH_load_timestamp"),
    "json_value.*",
)

df_deserialized.writeStream.format("iceberg").outputMode("append").trigger(
    once=True
).option("path", iceberg_table).option("fanout-enabled", "true").option(
    "checkpointLocation", checkpoint_location
).toTable(
    iceberg_table
).awaitTermination()


# query = df_deserialized.writeStream \
#     .format("iceberg") \
#     .outputMode("append") \
#     .trigger(processingTime='5 seconds') \
#     .option("checkpointLocation", checkpoint_location) \
#     .toTable(iceberg_table)
#     .awaitTermination()
#     # .option("path", iceberg_table) \
#     # .start()
