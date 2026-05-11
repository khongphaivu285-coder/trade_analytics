# =========================
# VALIDATE REQUIRED COLUMNS
# =========================

def validate_columns(

    df,

    required_columns
):

    missing = [

        col

        for col in required_columns

        if col not in df.columns
    ]

    if missing:

        raise ValueError(

            f"""
            Missing columns:

            {missing}
            """
        )

    return True


# =========================
# VALIDATE PRIMARY KEY
# =========================

def validate_primary_key(

    df,

    primary_key
):

    if primary_key not in df.columns:

        raise ValueError(

            f"""
            Primary key not found:

            {primary_key}
            """
        )

    return True


# =========================
# VALIDATE DUPLICATE KEYS
# =========================

def validate_duplicate_keys(

    df,

    primary_key
):

    duplicated = df[
        df[primary_key]
        .duplicated()
    ]

    if len(duplicated) > 0:

        print(

            f"""
            WARNING:

            Duplicate primary keys found:

            {len(duplicated)}
            """
        )

    return True