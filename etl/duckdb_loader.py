from database.connection import (

    get_connection
)

from config.tables import TABLES


# =========================
# LOAD PARQUET TO DUCKDB
# =========================

def load_duckdb():

    conn = get_connection()

    for table_name in TABLES:

        parquet_path = (

            f"data/parquet/{table_name}.parquet"
        )

        print(

            f"""
            Loading:

            {table_name}
            """
        )

        query = f"""

        CREATE OR REPLACE TABLE
        {table_name}

        AS

        SELECT *

        FROM read_parquet(
            '{parquet_path}'
        )

        """

        conn.execute(query)

    print(

        """
        DuckDB build success
        """
    )