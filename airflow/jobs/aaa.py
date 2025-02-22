from pyspark.sql import SparkSession
import time
# Initialize Spark session
spark = SparkSession.builder.appName('example').getOrCreate()

print(spark.version, 1111111111)

spark.sql(
"""
CREATE TABLE IF NOT EXISTS raw.customers (
    DWH_Snapshot_DT TIMESTAMP NOT NULL,
    CustomerID STRING NOT NULL COMMENT 'PK',
    FirstName  STRING,
    MiddleInitial   STRING,
    LastName STRING
    )
USING iceberg
PARTITIONED BY (DWH_Snapshot_DT)
"""
)