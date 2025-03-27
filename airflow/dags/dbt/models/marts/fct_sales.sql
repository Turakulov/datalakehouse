
{{
    config(
        enabled=true,
        materialized="table",
        database="vertica",
        schema="marts",
        sort="SalesID"
    )
}}


select
      now()             as DWH_LMD_timestamp
    , s.SalesID         as ProductID
    , s.CustomerID      as CustomerID
    , s.SalesPersonID   as SalesPersonID
    , s.ProductID       as ProductID
    , s.Quantity        as ProductQuantity
    , p.Price           as ProductPrice
    , s.Quantity * p.Price as TotalPrice
    , p.Name            as ProductName
    , c.LastName        as CustomerLastName
    , c.FirstName       as CustomerFirstName
    , c.MiddleInitial   as CustomerMiddleInitial
    , e.LastName        as SalesPersonLastName
    , e.FirstName       as SalesPersonFirstName
    , e.MiddleInitial   as SalesPersonMiddleInitial
from {{ ref('ods', 'ods_sales') }} as s
left join {{ ref('ods', 'ods_customers') }} as c
on s.CustomerID = c.CustomerID
left join {{ ref('ods', 'ods_employees') }} as e
on s.SalesPersonID = e.EmployeeID
left join {{ ref('ods', 'ods_products') }} as p
on s.ProductID = p.ProductID
