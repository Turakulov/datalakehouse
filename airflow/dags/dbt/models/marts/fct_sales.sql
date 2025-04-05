
{{
    config(
        enabled=true,
        materialized="table",
        database="vertica",
        schema="marts",
        order_by="SalesID",
        segmented_by_string="SalesID",
        partition_by_string='DWH_LMD_timestamp',
        depends_on=['ods_sales', 'ods_customers','ods_employees','ods_products']
    )
}}


select
    cast(now() as DATE)   as DWH_LMD_timestamp
    , s.SalesID         as SalesID
    , s.CustomerID      as CustomerID
    , s.SalesPersonID   as SalesPersonID
    , s.ProductID       as ProductID
    , s.Quantity        as ProductQuantity
    , p.Name            as ProductName
    , p.Price           as ProductPrice
    , c.LastName        as CustomerLastName
    , c.FirstName       as CustomerFirstName
    , c.MiddleInitial   as CustomerMiddleInitial
    , e.LastName        as SalesPersonLastName
    , e.FirstName       as SalesPersonFirstName
    , e.MiddleInitial   as SalesPersonMiddleInitial
from nessie.ods.ods_sales as s
left join nessie.ods.ods_customers as c
on s.CustomerID = c.CustomerID
left join nessie.ods.ods_employees as e
on s.SalesPersonID = e.EmployeeID
left join nessie.ods.ods_products as p
on s.ProductID = p.ProductID
