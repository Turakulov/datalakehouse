
{{
    config(
        enabled=true,
        materialized="table",
        database="nessie",
        schema="ods",
        properties= {
          "format": "'PARQUET'",
          "location": "'s3://warehouse/ods/ods_products'",
          "partitioning": "ARRAY['day(DWH_source_timestamp)']",
          "sorted_by": "ARRAY['ProductID']"
        }
    )
}}

select DWH_kafka_timestamp as DWH_source_timestamp
    , DWH_load_timestamp
    , ProductID
    , Name
    , Price
from (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY ProductID ORDER BY DWH_kafka_offset DESC) AS rn
    FROM {{ source('raw','products') }}
) t
WHERE rn = 1
