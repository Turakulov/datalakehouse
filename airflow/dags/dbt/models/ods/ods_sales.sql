
{{
    config(
        enabled=true,
        materialized="table",
        database="nessie",
        schema="ods",
        properties= {
          "format": "'PARQUET'",
          "location": "'s3://warehouse/ods/ods_sales'",
          "partitioning": "ARRAY['day(DWH_source_timestamp)']",
          "sorted_by": "ARRAY['SalesID']"
        }
    )
}}

select DWH_kafka_timestamp as DWH_source_timestamp
    , DWH_load_timestamp
    , CustomerID
    , SalesPersonID
    , SalesID
    , ProductID
    , Quantity
from (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY SalesID ORDER BY DWH_kafka_offset DESC) AS rn
    FROM {{ source('raw','sales') }}
) t
WHERE rn = 1
