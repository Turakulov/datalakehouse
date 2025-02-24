import json

from pyspark.sql.types import (
    IntegerType,
    StringType,
    StructType,
    StructField,
    FloatType,
    LongType,
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


database = "dwh"
iceberg_table_list = ["customers", "employees"]
for t in iceberg_table_list:
    message_schema = get_kafka_message_schema(topic=t)
    print(message_schema)
    create_table_sql = generate_create_table_sql(message_schema, t)
    print(create_table_sql)