import pandas as pd


# =========================================
# COMMON FILTER
# =========================================

def apply_common_filter(

    df_filtered,
    df_master
):

    # =====================================
    # COPY
    # =====================================

    filtered_df = df_filtered.copy()

    master_df = df_master.copy()

    # =====================================
    # DATETIME
    # =====================================

    filtered_df["orderdate2"] = pd.to_datetime(
        filtered_df["orderdate2"]
    )

    master_df["orderdate2"] = pd.to_datetime(
        master_df["orderdate2"]
    )

    # =====================================
    # KEEP NON-TIME FILTER
    # =====================================

    filter_columns = [

        "kênh",

        "tbd_line_name",

        "nhóm_khách_hàng",

        "khu_vực",

        "chain_3"
    ]

    result_df = master_df.copy()

    for col in filter_columns:

        selected_values = (
            filtered_df[col]
            .dropna()
            .unique()
            .tolist()
        )

        if len(selected_values) > 0:

            result_df = result_df[
                result_df[col]
                .isin(selected_values)
            ]

    # =====================================
    # BUSINESS FILTER
    # =====================================

    result_df = result_df[

        (result_df["ordertype1"] == "BÁN")

        # &

        # (result_df["kênh"] == "1. MT")
    ]

    return result_df


# =========================================
# YTD ORDER VALUE
# =========================================

def YTD_OrderValue(df):

    # =====================================
    # PREPARE
    # =====================================

    df = prepare_df(df)

    # =====================================
    # CURRENT DATE
    # =====================================

    max_date = (
        df["orderdate2"]
        .max()
    )

    current_year = (
        max_date.year
    )

    # =====================================
    # YTD FILTER
    # =====================================

    df = df[

        (df["orderdate2"].dt.year == current_year)

        &

        (
            df["orderdate2"]
            <= max_date
        )
    ]

    # =====================================
    # RETURN
    # =====================================

    return df["ordervalue"].sum()


# =========================================
# YTD LY ORDER VALUE
# =========================================

def YTD_LY_OrderValue(df):

    # =====================================
    # PREPARE
    # =====================================

    df = prepare_df(df)

    # =====================================
    # CURRENT DATE
    # =====================================

    max_date = (
        df["orderdate2"]
        .max()
    )

    # =====================================
    # LY DATE
    # =====================================

    ly_max_date = (
        max_date
        - pd.DateOffset(years=1)
    )

    ly_year = (
        ly_max_date.year
    )

    # =====================================
    # LY FILTER
    # =====================================

    df = df[

        (df["orderdate2"].dt.year == ly_year)

        &

        (
            df["orderdate2"]
            <= ly_max_date
        )
    ]

    # =====================================
    # RETURN
    # =====================================

    return df["ordervalue"].sum()


# =========================================
# YTD YOY GROWTH
# =========================================

def YTD_YoY_Growth(df):

    # =====================================
    # CURRENT VALUE
    # =====================================

    current_value = (
        YTD_OrderValue(df)
    )

    # =====================================
    # LY VALUE
    # =====================================

    ly_value = (
        YTD_LY_OrderValue(df)
    )

    # =====================================
    # DIVIDE BY ZERO
    # =====================================

    if ly_value == 0:

        return 0

    # =====================================
    # YOY %
    # =====================================

    growth = (

        (
            current_value
            - ly_value
        )

        / ly_value

    ) * 100

    # =====================================
    # RETURN
    # =====================================

    return round(growth, 2)


# =========================================
# TOTAL VOLUME
# =========================================

def Total_Volume(df):

    # =====================================
    # PREPARE
    # =====================================

    df = prepare_df(df)

    # =====================================
    # CURRENT DATE
    # =====================================

    max_date = (
        df["orderdate2"]
        .max()
    )

    # =====================================
    # FILTER TO CURRENT
    # =====================================

    df = df[

        df["orderdate2"]
        <= max_date
    ]

    # =====================================
    # RETURN
    # =====================================

    return df["ordervalue"].sum()

# =========================================
# YTD TREND 13 MONTHS
# =========================================

def YTD_Trend_13M(df):

    # =====================================
    # PREPARE
    # =====================================

    df = prepare_df(df)

    # =====================================
    # YEAR MONTH
    # =====================================

    df["YearMonth"] = (
        df["orderdate2"]
        .dt.to_period("M")
        .astype(str)
    )

    # =====================================
    # MONTHLY SALES
    # =====================================

    trend_df = (

        df.groupby(
            "YearMonth",
            as_index=False
        )["ordervalue"]
        .sum()
        .sort_values("YearMonth")
        .tail(13)
    )

    # =====================================
    # RETURN
    # =====================================

    return {

        "categories": (
            trend_df["YearMonth"]
            .tolist()
        ),

        "values": (
            trend_df["ordervalue"]
            .round(0)
            .tolist()
        )
    }

# =========================================
# BASE PREPARE
# =========================================

def prepare_df(df):

    df = df.copy()

    df["orderdate2"] = pd.to_datetime(
        df["orderdate2"]
    )

    # =====================================
    # BUSINESS RULE
    # =====================================

    df = df[
        df["ordertype1"] == "BÁN"
    ]

    return df


# =========================================
# YTD ORDER VALUE - GLOBAL
# =========================================

def YTD_OrderValue_Global(df):

    df = prepare_df(df)

    max_date = (
        df["orderdate2"]
        .max()
    )

    current_year = (
        max_date.year
    )

    df = df[

        (df["orderdate2"].dt.year == current_year)

        &

        (
            df["orderdate2"]
            <= max_date
        )
    ]

    return df["ordervalue"].sum()


# =========================================
# YTD LY ORDER VALUE - GLOBAL
# =========================================

def YTD_LY_OrderValue_Global(df):

    df = prepare_df(df)

    max_date = (
        df["orderdate2"]
        .max()
    )

    ly_max_date = (
        max_date
        - pd.DateOffset(years=1)
    )

    ly_year = (
        ly_max_date.year
    )

    df = df[

        (df["orderdate2"].dt.year == ly_year)

        &

        (
            df["orderdate2"]
            <= ly_max_date
        )
    ]

    return df["ordervalue"].sum()


# =========================================
# YTD YOY GROWTH - GLOBAL
# =========================================

def YTD_YoY_Growth_Global(df):

    current_value = (
        YTD_OrderValue_Global(df)
    )

    ly_value = (
        YTD_LY_OrderValue_Global(df)
    )

    if ly_value == 0:

        return 0

    growth = (

        (
            current_value
            - ly_value
        )

        / ly_value

    ) * 100

    return round(growth, 2)


# =========================================
# CURRENT MONTH ORDER VALUE
# =========================================

def CurrentMonth_OrderValue_Global(df):

    df = prepare_df(df)

    max_date = (
        df["orderdate2"]
        .max()
    )

    current_period = (
        max_date.to_period("M")
    )

    df = df[

        df["orderdate2"]
        .dt.to_period("M")
        == current_period
    ]

    return df["ordervalue"].sum()


# =========================================
# CURRENT MONTH VS LY
# =========================================

def CurrentMonth_vs_LY_Global(df):

    df = prepare_df(df)

    max_date = (
        df["orderdate2"]
        .max()
    )

    current_period = (
        max_date.to_period("M")
    )

    ly_period = (
        current_period - 12
    )

    current_value = (

        df[
            df["orderdate2"]
            .dt.to_period("M")
            == current_period
        ]["ordervalue"]
        .sum()
    )

    ly_value = (

        df[
            df["orderdate2"]
            .dt.to_period("M")
            == ly_period
        ]["ordervalue"]
        .sum()
    )

    if ly_value == 0:

        return 0

    growth = (

        (
            current_value
            - ly_value
        )

        / ly_value

    ) * 100

    return round(growth, 2)


# =========================================
# CURRENT MONTH VS LAST MONTH
# =========================================

def CurrentMonth_vs_LastMonth_Global(df):

    df = prepare_df(df)

    max_date = (
        df["orderdate2"]
        .max()
    )

    current_period = (
        max_date.to_period("M")
    )

    prev_period = (
        current_period - 1
    )

    current_value = (

        df[
            df["orderdate2"]
            .dt.to_period("M")
            == current_period
        ]["ordervalue"]
        .sum()
    )

    prev_value = (

        df[
            df["orderdate2"]
            .dt.to_period("M")
            == prev_period
        ]["ordervalue"]
        .sum()
    )

    if prev_value == 0:

        return 0

    growth = (

        (
            current_value
            - prev_value
        )

        / prev_value

    ) * 100

    return round(growth, 2)


# =========================================
# CURRENT MONTH VS AVG 3M
# =========================================

def CurrentMonth_vs_Avg3M_Global(df):

    df = prepare_df(df)

    df["YearMonth"] = (
        df["orderdate2"]
        .dt.to_period("M")
    )

    monthly_df = (

        df.groupby(
            "YearMonth",
            as_index=False
        )["ordervalue"]
        .sum()
        .sort_values("YearMonth")
    )

    current_period = (
        monthly_df["YearMonth"]
        .max()
    )

    current_value = (

        monthly_df[
            monthly_df["YearMonth"]
            == current_period
        ]["ordervalue"]
        .iloc[0]
    )

    avg_3m = (

        monthly_df[
            monthly_df["YearMonth"]
            < current_period
        ]
        .tail(3)["ordervalue"]
        .mean()
    )

    if avg_3m == 0:

        return 0

    growth = (

        (
            current_value
            - avg_3m
        )

        / avg_3m

    ) * 100

    return round(growth, 2)


# =========================================
# CURRENT MONTH VS AVG 6M
# =========================================

def CurrentMonth_vs_Avg6M_Global(df):

    df = prepare_df(df)

    df["YearMonth"] = (
        df["orderdate2"]
        .dt.to_period("M")
    )

    monthly_df = (

        df.groupby(
            "YearMonth",
            as_index=False
        )["ordervalue"]
        .sum()
        .sort_values("YearMonth")
    )

    current_period = (
        monthly_df["YearMonth"]
        .max()
    )

    current_value = (

        monthly_df[
            monthly_df["YearMonth"]
            == current_period
        ]["ordervalue"]
        .iloc[0]
    )

    avg_6m = (

        monthly_df[
            monthly_df["YearMonth"]
            < current_period
        ]
        .tail(6)["ordervalue"]
        .mean()
    )

    if avg_6m == 0:

        return 0

    growth = (

        (
            current_value
            - avg_6m
        )

        / avg_6m

    ) * 100

    return round(growth, 2)