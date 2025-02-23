from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Jupyter").getOrCreate()

# Taking a quick peek at the vertica-data2, you can see that there are a number of permits for different boroughs in New York.
spark.read.format("iceberg").load("nyc.permits").groupBy("data").count().show()
