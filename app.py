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
# NORMALIZE BLANK VALUE
# =========================================

filter_columns = [

    "kênh",

    "tbd_line_name",

    "khu_vực",

    "nhóm_khách_hàng",

    "chain_3"
]

for col in filter_columns:

    master_df[col] = (

        master_df[col]

        .fillna("BLANK")

        .replace("", "BLANK")

        .astype(str)
        .str.strip()
        .replace("nan", "BLANK")
    )

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
        "dashboards/overview/Untitled (1).png",
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

    if not selected:
        return "ALL"

    if set(selected) == set(available):
        return "ALL"

    if len(selected) <= 3:
        return ", ".join(map(str, selected))

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

    available_channel = sorted(
        master_df["kênh"]
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
    
        with st.expander(
            "Năm - Tháng",
            expanded=False
        ):
    
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
    
            selected_months = st.multiselect(
                "Chọn tháng",
                options=available_months,
                default=available_months
            )
    
    st.divider()

    # =====================================
    # DEFAULT CHANNEL
    # =====================================

    default_channel = (
        ["1. MT"]
        if "1. MT" in available_channel
        else available_channel
    )

    # =====================================
    # INIT SESSION STATE
    # =====================================

    if "selected_channel" not in st.session_state:

        st.session_state["selected_channel"] = (
            default_channel
        )

    # =====================================
    # CHANNEL FILTER
    # =====================================

    selected_channel = st.multiselect(
        "Kênh",
        options=available_channel,
        key="selected_channel"
    )

    # =====================================
    # DETECT CHANNEL CHANGE
    # =====================================

    current_channel_key = "|".join(
        sorted(selected_channel)
    )

    previous_channel_key = (
        st.session_state.get(
            "previous_channel_key",
            ""
        )
    )

    # =====================================
    # CHANNEL FILTERED DATA
    # =====================================

    channel_filtered_df = master_df[
        master_df["kênh"]
        .isin(selected_channel)
    ]

    # =====================================
    # CASCADE AVAILABLE VALUES
    # =====================================

    available_line = sorted(
        channel_filtered_df["tbd_line_name"]
        .unique()
        .tolist()
    )

    available_region = sorted(
        channel_filtered_df["khu_vực"]
        .unique()
        .tolist()
    )

    available_group = sorted(
        channel_filtered_df["nhóm_khách_hàng"]
        .unique()
        .tolist()
    )

    available_chain_3 = sorted(
        channel_filtered_df["chain_3"]
        .unique()
        .tolist()
    )

    # =====================================
    # RESET BUSINESS FILTERS
    # =====================================

    if current_channel_key != previous_channel_key:

        # =================================
        # REMOVE OLD FILTER STATE
        # =================================

        for key in [

            "selected_line",

            "selected_region",

            "selected_group",

            "selected_chain_3"
        ]:

            if key in st.session_state:

                del st.session_state[key]

        # =================================
        # SELECT ALL NEW VALUES
        # =================================

        st.session_state["selected_line"] = (
            available_line
        )

        st.session_state["selected_region"] = (
            available_region
        )

        st.session_state["selected_group"] = (
            available_group
        )

        st.session_state["selected_chain_3"] = (
            available_chain_3
        )

        # =================================
        # UPDATE CHANNEL KEY
        # =================================

        st.session_state["previous_channel_key"] = (
            current_channel_key
        )

        st.rerun()

    # =====================================
    # INIT FILTER STATE
    # =====================================

    if "selected_line" not in st.session_state:

        st.session_state["selected_line"] = (
            available_line
        )

    if "selected_region" not in st.session_state:

        st.session_state["selected_region"] = (
            available_region
        )

    if "selected_group" not in st.session_state:

        st.session_state["selected_group"] = (
            available_group
        )

    if "selected_chain_3" not in st.session_state:

        st.session_state["selected_chain_3"] = (
            available_chain_3
        )

    # =====================================
    # OTHER FILTERS
    # =====================================

    with st.expander(
        "Lọc theo các yếu tố khác",
        expanded=False
    ):

        filter_col_1, filter_col_2 = st.columns(2)

        with filter_col_1:

            selected_line = st.multiselect(
                "Dòng sản phẩm",
                options=available_line,
                key="selected_line"
            )

        with filter_col_2:

            selected_region = st.multiselect(
                "Khu vực",
                options=available_region,
                key="selected_region"
            )

        filter_col_3, filter_col_4 = st.columns(2)

        with filter_col_3:

            selected_group = st.multiselect(
                "Nhóm khách hàng",
                options=available_group,
                key="selected_group"
            )

        with filter_col_4:

            selected_chain_3 = st.multiselect(
                "Chuỗi",
                options=available_chain_3,
                key="selected_chain_3"
            )

    # =====================================
    # SUMMARY
    # =====================================

    summary_col_1, summary_col_2, summary_col_3, summary_col_4, summary_col_5 = st.columns(5)

    with summary_col_1:

        st.caption(
            f"Dòng sản phẩm: {filter_label(selected_line, available_line)}"
        )

    with summary_col_2:

        st.caption(
            f"Khu vực: {filter_label(selected_region, available_region)}"
        )

    with summary_col_3:

        st.caption(
            f"Nhóm khách hàng: {filter_label(selected_group, available_group)}"
        )

    with summary_col_4:

        st.caption(
            f"Chuỗi: {filter_label(selected_chain_3, available_chain_3)}"
        )

    with summary_col_5:

        st.caption(
            f"Kênh: {filter_label(selected_channel, available_channel)}"
        )

# =========================================
# APPLY FILTER
# =========================================

filtered_df = master_df.copy()

# =========================================
# KPI / GLOBAL TIME INTELLIGENCE
# -> KHÔNG bị ảnh hưởng bởi year/month slicer
# =========================================

business_filtered_df = master_df.copy()

# =========================================
# YEAR FILTER
# -> chỉ apply cho visual/table
# =========================================

if set(selected_years) != set(available_years):

    filtered_df = filtered_df[
        filtered_df["order_year"]
        .isin(selected_years)
    ]

# =========================================
# CHANNEL
# =========================================

if set(selected_channel) != set(available_channel):

    filtered_df = filtered_df[
        filtered_df["kênh"]
        .isin(selected_channel)
    ]

    business_filtered_df = business_filtered_df[
        business_filtered_df["kênh"]
        .isin(selected_channel)
    ]

# =========================================
# LINE
# =========================================

if set(selected_line) != set(available_line):

    filtered_df = filtered_df[
        filtered_df["tbd_line_name"]
        .isin(selected_line)
    ]

    business_filtered_df = business_filtered_df[
        business_filtered_df["tbd_line_name"]
        .isin(selected_line)
    ]

# =========================================
# REGION
# =========================================

if set(selected_region) != set(available_region):

    filtered_df = filtered_df[
        filtered_df["khu_vực"]
        .isin(selected_region)
    ]

    business_filtered_df = business_filtered_df[
        business_filtered_df["khu_vực"]
        .isin(selected_region)
    ]

# =========================================
# CUSTOMER GROUP
# =========================================

if set(selected_group) != set(available_group):

    filtered_df = filtered_df[
        filtered_df["nhóm_khách_hàng"]
        .isin(selected_group)
    ]

    business_filtered_df = business_filtered_df[
        business_filtered_df["nhóm_khách_hàng"]
        .isin(selected_group)
    ]

# =========================================
# CHAIN 3
# =========================================

if set(selected_chain_3) != set(available_chain_3):

    filtered_df = filtered_df[
        filtered_df["chain_3"]
        .isin(selected_chain_3)
    ]

    business_filtered_df = business_filtered_df[
        business_filtered_df["chain_3"]
        .isin(selected_chain_3)
    ]

# =========================================
# YEAR MONTH
# =========================================

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

# =========================================
# MONTH FILTER
# -> KHÔNG apply cho business_filtered_df
# =========================================

if set(selected_months) != set(available_months):

    filtered_df = filtered_df[
        filtered_df["year_month"]
        .isin(selected_months)
    ]

# =========================================
# OPTIONAL:
# tránh SettingWithCopyWarning
# =========================================

filtered_df = filtered_df.copy()

business_filtered_df = business_filtered_df.copy()

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
        master_df,
        business_filtered_df
    )

elif page == "📦 By Product":

    show_overview(
        filtered_df,
        master_df,
        business_filtered_df
    )

elif page == "🏪 By Account":

    show_overview(
        filtered_df,
        master_df,
        business_filtered_df
    )