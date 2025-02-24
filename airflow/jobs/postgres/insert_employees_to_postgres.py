from pyspark.sql import SparkSession

# 🔹 1. Настроим Spark с поддержкой Iceberg и S3
spark = SparkSession.builder \
    .appName("IcebergToPostgres") \
    .getOrCreate()

# 🔹 2. Читаем таблицу Iceberg из S3 (MinIO)
iceberg_table = "dwh.employees"
df = spark.read.format("iceberg").load(iceberg_table)

# 🔹 3. Настройки PostgreSQL
postgres_url = "jdbc:postgresql://host.docker.internal:5432/postgres_db"
postgres_properties = {
    "user": "postgres_user",
    "password": "postgres_password",
    "driver": "org.postgresql.Driver"
}

# 🔹 4. Записываем данные в PostgreSQL
df.write \
    .format("jdbc") \
    .option("url", postgres_url) \
    .option("dbtable", "raw.employees") \
    .option("user", postgres_properties["user"]) \
    .option("password", postgres_properties["password"]) \
    .option("driver", postgres_properties["driver"]) \
    .mode("append") \
    .save()

print("✅ Data successfully loaded from Iceberg (MinIO S3) to PostgreSQL!")

# 🔹 5. Останавливаем Spark
spark.stop()