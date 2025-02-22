from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Jupyter").getOrCreate()

spark.sql("CREATE DATABASE IF NOT EXISTS nyc")
spark.sql("DROP TABLE IF EXISTS nyc.permits")

df = spark.read.option("inferSchema","true").option("multiline","true").json("/home/iceberg/data/nyc_film_permits.json")
print(df.head())
df.write.saveAsTable("nyc.permits")