
{{
    config(
        enabled=true,
        materialized="table",
        database="nessie",
        schema="ods",
        properties= {
          "format": "'PARQUET'",
          "location": "'s3://warehouse/ods/ods_customers'",
          "partitioning": "ARRAY['day(DWH_source_timestamp)']",
          "sorted_by": "ARRAY['CustomerID']"
        }
    )
}}

SELECT DWH_kafka_timestamp  as DWH_source_timestamp
    , DWH_load_timestamp
    , CustomerID
    , LastName
    , FirstName
    , MiddleInitial
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY DWH_kafka_offset DESC) AS rn
    FROM {{ source('raw','customers') }}
) t
WHERE rn = 1
