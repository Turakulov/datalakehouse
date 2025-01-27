from pyspark.sql import SparkSession
from pyspark.sql.functions import  broadcast, expr, col
import pickle


with open('data.pickle', 'rb') as handle:
    data = pickle.load(handle)

print(data.keys())
print(data['Customers'] , type(data['Customers']))

data['Customers'].to_csv('./data.csv')

# with open('metadata.pickle', 'rb') as handle:
#     metadata = pickle.load(handle)
#
# print(metadata)
# "columns": {
#                 "CustomerID": {
#                     "sdtype": "id"
#                 },
#                 "MiddleInitial": {
#                     "sdtype": "categorical"
#                 },
#                 "FirstName": {
#                     "sdtype": "categorical"
#                 },
#                 "LastName": {
#                     "sdtype": "categorical"
#                 }
#             },
#             "primary_key": "CustomerID"

# print(metadata['Customers'], type(metadata['Customers']))

# spark = SparkSession.builder \
#                     .appName("Jupyter") \
#                     .config("spark.sql.autoBroadcastJoinThreshold", "-1") \
#                     .getOrCreate()
# spark.sql(
#     """
# CREATE TABLE IF NOT EXISTS raw.customers (
#     DWH_Snapshot_DT TIMESTAMP NOT NULL,
#     CustomerID BIGINT NOT NULL COMMENT 'PK',
#     FirstName  STRING,
#     MiddleInitial   STRING,
#     LastName STRING
#     )
# USING iceberg
# PARTITIONED BY (day(DWH_Snapshot_DT))
# """
# )
# df_spark = spark.createDataFrame(data['Customers'])
#
# df_spark.show()
# df_spark.write.mode("append").saveAsTable("raw.customer")