from etl.extract import load_excel

from etl.transform import (

    standardize_columns
)
    
from etl.validate import (

    validate_columns,

    validate_primary_key,

    validate_duplicate_keys
)

from config.tables import TABLES


# =========================
# LOAD DATA
# =========================

table_name = "purchase_order"

df = load_excel(table_name)

# =========================
# STANDARDIZE
# =========================

df = standardize_columns(df)

# =========================
# GET CONFIG
# =========================

config = TABLES[table_name]

required_columns = config[
    "required_columns"
]

primary_key = config[
    "primary_key"
]

# =========================
# VALIDATIONS
# =========================

validate_columns(

    df,

    required_columns
)

validate_primary_key(

    df,

    primary_key
)

validate_duplicate_keys(

    df,

    primary_key
)

print(

    "Validation success"
)