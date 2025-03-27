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
          "sorted_by": "ARRAY['EmployeeID']"
        }
    )
}}

select DWH_kafka_timestamp as DWH_source_timestamp
    , DWH_load_timestamp
    , EmployeeID
    , LastName
    , FirstName
    , MiddleInitial
from (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY EmployeeID ORDER BY DWH_kafka_offset DESC) AS rn
    FROM {{ source('raw','employees') }}
) t
WHERE rn = 1
