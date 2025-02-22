select  DWH_kafka_key
, DWH_kafka_partition
, DWH_kafka_offset
, DWH_kafka_timestamp
, DWH_load_timestamp
, MiddleInitial
, FirstName
, EmployeeID
, LastName
from {{ source('stage','employees')}}
limit 1 over (partition by EmployeeID order by DWH_kafka_offset desc)
