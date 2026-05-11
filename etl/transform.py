import pandas as pd


# =========================
# STANDARDIZE COLUMN NAMES
# =========================

def standardize_columns(df):

    df.columns = [

        str(col)

        .strip()

        .replace(" ", "_")

        .replace("-", "_")

        .replace("/", "_")

        .replace("(", "")

        .replace(")", "")

        .replace(".", "")

        .lower()

        for col in df.columns
    ]

    return df


# =========================
# CONVERT DATE COLUMNS
# =========================

def convert_dates(

    df,

    date_columns
):

    for col in date_columns:

        if col in df.columns:

            df[col] = pd.to_datetime(

                df[col],

                errors="coerce"
            )

    return df


# =========================
# REMOVE DUPLICATES
# =========================

def remove_duplicates(

    df,

    primary_key
):

    if primary_key in df.columns:

        df = df.drop_duplicates(

            subset=[primary_key]
        )

    return df


def add_date_columns(df):

    df = df.copy()

    df["OrderDate2"] = pd.to_datetime(df["OrderDate2"])

    df["Year"] = df["OrderDate2"].dt.year

    df["MonthNo"] = df["OrderDate2"].dt.month

    df["Month"] = (
        "Tháng "
        + df["MonthNo"].astype(str)
    )

    df["YearMonth"] = (
        df["Year"].astype(str)
        + "-"
        + df["MonthNo"].astype(str).str.zfill(2)
    )

    df["YearMonthSort"] = (
        df["Year"] * 100
        + df["MonthNo"]
    )

    return df