from database.connection import (
    get_connection
)

conn = get_connection()

query = """

DESCRIBE purchase_order

"""

df = conn.execute(query).df()

print(df)