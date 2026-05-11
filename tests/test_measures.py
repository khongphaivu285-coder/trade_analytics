from business_logic.measures.sales_measures import (

    total_sales,

    total_cs_quantity,

    total_customers,

    avg_sales_per_customer,

    ytd_sales
)


print(

    "Total Sales:",
    total_sales()
)

print(

    "Total CS Qty:",
    total_cs_quantity()
)

print(

    "Customers:",
    total_customers()
)

print(

    "Avg Sales Per Customer:",
    avg_sales_per_customer()
)

print(

    "YTD Sale:",
    ytd_sales()
)

