import duckdb


# =========================
# GET DATABASE CONNECTION
# =========================

def get_connection():

    conn = duckdb.connect(

        "data/duckdb/analytics.duckdb"
    )

    return conn