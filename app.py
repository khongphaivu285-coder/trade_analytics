import streamlit as st

from dashboards.overview.overview_page import (
    show_overview
)

from dashboards.by_product.by_product_page import (
    show_by_product
)

from dashboards.by_account.by_account_page import (
    show_by_account
)

from models.sales_model import sales_model

from business_logic.cross_filter.pie_cross_filter import (

    initialize_pie_filters
)

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Goody Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================
# GLOBAL LAYOUT CONFIG
# =========================================

APP_WIDTH = 1289

APP_PADDING_TOP = 58
APP_PADDING_RIGHT = 18
APP_PADDING_BOTTOM = 18
APP_PADDING_LEFT = 18

CARD_GAP = 5

# =========================================
# GLOBAL CSS
# =========================================

st.markdown(
    f"""
    <style>

    .stApp {{

        background-color: #FFFFFF;
    }}

    /* ====================================
       HEADER
    ==================================== */

    header {{

        background: transparent;

        height: 0px;
    }}

    #MainMenu {{

        display: none;
    }}

    footer {{

        visibility: hidden;
    }}

    [data-testid="collapsedControl"] {{

        display: block !important;
    }}

    /* ====================================
       SIDEBAR
    ==================================== */

    section[data-testid="stSidebar"] {{

        background: #172338;

        border-right: 1px solid rgba(255,255,255,0.06);
    }}

    section[data-testid="stSidebar"] * {{

        color: white !important;
    }}

    .stRadio label {{

        padding: 12px 14px;

        border-radius: 12px;

        transition: all 0.2s ease;
    }}

    .stRadio label:hover {{

        background: rgba(255,255,255,0.06);
    }}

    /* ====================================
       MAIN CONTAINER
    ==================================== */

    .block-container {{

        max-width: {APP_WIDTH}px;

        min-width: {APP_WIDTH}px;

        padding-top: {APP_PADDING_TOP}px;

        padding-right: {APP_PADDING_RIGHT}px;

        padding-bottom: {APP_PADDING_BOTTOM}px;

        padding-left: {APP_PADDING_LEFT}px;
    }}

    [data-testid="column"] {{

        padding-left: {CARD_GAP / 2}px;

        padding-right: {CARD_GAP / 2}px;
    }}

    /* ====================================
       CARD
    ==================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {{

        background-color: transparent !important;

        border-radius: 22px !important;

        border: 1px solid rgba(0,0,0,0.05) !important;

        box-shadow:
            0px 4px 12px rgba(0,0,0,0.04),
            0px 10px 24px rgba(0,0,0,0.06) !important;

        overflow: hidden !important;
    }}

    /* ====================================
       TOP BAR
    ==================================== */

    .top-bar {{

        width: 100%;

        height: 54px;

        background: #354E7B;

        border-radius: 22px;
    }}

    /* ====================================
       TYPOGRAPHY
    ==================================== */

    h3 {{

        margin-bottom: 0rem !important;

        padding-bottom: 0rem !important;
    }}

    [data-testid="stMetric"] {{

        margin-top: -18px;
    }}

    [data-testid="stMetricLabel"] {{

        display: none;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================
# LOAD MASTER DATA
# =========================================

master_df = sales_model()

# =========================================
# INIT PIE FILTER
# =========================================

initialize_pie_filters()

# =========================================
# SIDEBAR NAVIGATION
# =========================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:28px;
            font-weight:700;
            padding-top:10px;
            padding-bottom:24px;
        ">
            📊 Goody Dashboard
        </div>
        """,
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        [
            "📈 Tổng quan",
            "📦 By Product",
            "🏪 By Account"
        ]
    )

# =========================================
# HEADER
# =========================================

header_left, header_right = st.columns([2, 8])

with header_left:

    st.image(
        r"D:\trade_analytics\dashboards\overview\Untitled (1).png",
        width=250
    )

with header_right:

    st.markdown(
        """
        <div style="
            height:54px;
            display:flex;
            align-items:center;
        ">
            <div class="top-bar"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================
# HEADER GAP
# =========================================

st.markdown(
    f"<div style='height:{CARD_GAP}px'></div>",
    unsafe_allow_html=True
)

# =========================================
# FILTER LABEL
# =========================================

def filter_label(selected, available):

    if len(selected) == 0:

        return "ALL"

    if set(selected) == set(available):

        return "ALL"

    if len(selected) == 1:

        return str(selected[0])

    return f"{len(selected)} selected"


# =========================================
# GLOBAL FILTER
# =========================================

with st.container(
    border=True
):

    # =====================================
    # AVAILABLE VALUES
    # =====================================

    available_years = sorted(
        master_df["order_year"]
        .dropna()
        .unique()
        .tolist()
    )

    available_line = sorted(
        master_df["tbd_line_name"]
        .dropna()
        .unique()
        .tolist()
    )

    available_region = sorted(
        master_df["khu_vực"]
        .dropna()
        .unique()
        .tolist()
    )

    available_group = sorted(
        master_df["nhóm_khách_hàng"]
        .dropna()
        .unique()
        .tolist()
    )

    available_chain_3 = sorted(
        master_df["chain_3"]
        .dropna()
        .unique()
        .tolist()
    )

    # =====================================
    # TIME FILTER
    # =====================================

    st.subheader(
        "Bộ lọc theo thời gian"
    )

    time_col_1, time_col_2 = st.columns(2)

    with time_col_1:

        selected_years = st.multiselect(
            "Năm",
            options=available_years,
            default=available_years
        )

    with time_col_2:

        month_options = (
            master_df[
                master_df["order_year"]
                .isin(selected_years)
            ][[
                "order_year",
                "order_month"
            ]]
            .drop_duplicates()
            .sort_values([
                "order_year",
                "order_month"
            ])
        )

        month_options["label"] = (
            month_options["order_year"]
            .astype(int)
            .astype(str)

            + "-"

            +

            month_options["order_month"]
            .astype(int)
            .astype(str)
            .str.zfill(2)
        )

        available_months = (
            month_options["label"]
            .tolist()
        )

        with st.expander(
            "Bộ lọc Năm - Tháng",
            expanded=False
        ):

            selected_months = st.multiselect(
                "Năm - Tháng",
                options=available_months,
                default=available_months
            )

    st.divider()

    summary_col_1, summary_col_2, summary_col_3, summary_col_4 = st.columns(4)

    with summary_col_1:

        st.caption(
            f"Dòng sản phẩm: {filter_label(available_line, available_line)}"
        )

    with summary_col_2:

        st.caption(
            f"Khu vực: {filter_label(available_region, available_region)}"
        )

    with summary_col_3:

        st.caption(
            f"Nhóm khách hàng: {filter_label(available_group, available_group)}"
        )

    with summary_col_4:

        st.caption(
            f"Chuỗi: {filter_label(available_chain_3, available_chain_3)}"
        )

    with st.expander(
        "Lọc theo các yếu tố khác",
        expanded=False
    ):

        filter_col_1, filter_col_2 = st.columns(2)

        with filter_col_1:

            selected_line = st.multiselect(
                "Dòng sản phẩm",
                options=available_line,
                default=available_line
            )

        with filter_col_2:

            selected_region = st.multiselect(
                "Khu vực",
                options=available_region,
                default=available_region
            )

        filter_col_3, filter_col_4 = st.columns(2)

        with filter_col_3:

            selected_group = st.multiselect(
                "Nhóm khách hàng",
                options=available_group,
                default=available_group
            )

        with filter_col_4:

            selected_chain_3 = st.multiselect(
                "Chuỗi",
                options=available_chain_3,
                default=available_chain_3
            )

# =========================================
# APPLY FILTER
# =========================================

filtered_df = master_df.copy()

if set(selected_years) != set(available_years):

    filtered_df = filtered_df[
        filtered_df["order_year"]
        .isin(selected_years)
    ]

if set(selected_line) != set(available_line):

    filtered_df = filtered_df[
        filtered_df["tbd_line_name"]
        .isin(selected_line)
    ]

if set(selected_region) != set(available_region):

    filtered_df = filtered_df[
        filtered_df["khu_vực"]
        .isin(selected_region)
    ]

if set(selected_group) != set(available_group):

    filtered_df = filtered_df[
        filtered_df["nhóm_khách_hàng"]
        .isin(selected_group)
    ]

if set(selected_chain_3) != set(available_chain_3):

    filtered_df = filtered_df[
        filtered_df["chain_3"]
        .isin(selected_chain_3)
    ]

filtered_df["year_month"] = (

    filtered_df["order_year"]
    .astype(int)
    .astype(str)

    + "-"

    +

    filtered_df["order_month"]
    .astype(int)
    .astype(str)
    .str.zfill(2)
)

if set(selected_months) != set(available_months):

    filtered_df = filtered_df[
        filtered_df["year_month"]
        .isin(selected_months)
    ]


# =========================================
# HEADER GAP
# =========================================

st.markdown(
    f"<div style='height:{CARD_GAP}px'></div>",
    unsafe_allow_html=True
)

# =========================================
# PAGE RENDER
# =========================================

if page == "📈 Tổng quan":

    show_overview(
        filtered_df,
        master_df
    )

elif page == "📦 By Product":

    show_by_product(
        filtered_df,
        master_df
    )

elif page == "🏪 By Account":

    show_by_account(
        filtered_df,
        master_df
    )