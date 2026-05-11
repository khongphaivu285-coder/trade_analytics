from database.connection import (

    get_connection
)

conn = get_connection()


# =========================
# TEST QUERY
# =========================

query = """

SELECT

    customerid,

    SUM(ordervalue) AS total_sales

FROM purchase_order

GROUP BY customerid

LIMIT 10

"""


df = conn.execute(

    query

).df()


print(df)

print(df.columns)