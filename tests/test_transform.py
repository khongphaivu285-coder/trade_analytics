from etl.extract import load_excel

from etl.transform import (

    standardize_columns,

    convert_dates
)

from config.tables import TABLES


# =========================
# LOAD PURCHASE ORDER
# =========================

df = load_excel(

    "purchase_order"
)

# =========================
# STANDARDIZE COLUMNS
# =========================

df = standardize_columns(df)

# =========================
# CONVERT DATES
# =========================

date_columns = TABLES[
    "purchase_order"
].get(

    "date_columns",

    []
)

df = convert_dates(

    df,

    date_columns
)

# =========================
# TEST OUTPUT
# =========================

print(df.columns)

print(df.dtypes)

from etl.transform import (

    remove_duplicates
)

primary_key = TABLES[
    "purchase_order"
][
    "primary_key"
]

df = remove_duplicates(

    df,

    primary_key
)

print(df.shape)