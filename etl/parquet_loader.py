from etl.extract import load_excel

from etl.transform import (

    standardize_columns,

    convert_dates
)

from etl.validate import (

    validate_columns,

    validate_primary_key,

    validate_duplicate_keys
)

from config.tables import TABLES


# =========================
# CONVERT TABLE TO PARQUET
# =========================

def convert_to_parquet(

    table_name
):

    # =========================
    # LOAD CONFIG
    # =========================

    config = TABLES[table_name]

    # =========================
    # EXTRACT
    # =========================

    df = load_excel(table_name)

    # =========================
    # TRANSFORM
    # =========================

    df = standardize_columns(df)

    df = convert_dates(

        df,

        config.get(
            "date_columns",
            []
        )
    )

    # =========================
    # VALIDATE
    # =========================

    validate_columns(

        df,

        config[
            "required_columns"
        ]
    )

    validate_primary_key(

        df,

        config[
            "primary_key"
        ]
    )

    validate_duplicate_keys(

        df,

        config[
            "primary_key"
        ]
    )

    # =========================
    # SAVE PARQUET
    # =========================

    output_path = (

        f"data/parquet/{table_name}.parquet"
    )

    df.to_parquet(

        output_path,

        index=False
    )

    print(

        f"""
        Saved parquet:

        {output_path}

        Rows: {len(df):,}
        """
    )