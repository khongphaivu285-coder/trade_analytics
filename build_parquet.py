from etl.parquet_loader import (

    convert_to_parquet
)

from config.tables import TABLES


# =========================
# BUILD ALL PARQUET FILES
# =========================

for table_name in TABLES:

    print(

        f"""
        Processing:

        {table_name}
        """
    )

    convert_to_parquet(

        table_name
    )