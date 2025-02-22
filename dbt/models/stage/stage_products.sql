select  DWH_kafka_key
    , DWH_kafka_partition
    , DWH_kafka_offset
    , DWH_kafka_timestamp
    , DWH_load_timestamp
    , Name
    , Price
    , ProductID
from {{ source('stage','products')}}
limit 1 over (partition by ProductID order by DWH_kafka_offset desc)
