import streamlit as st

from models.sales_model import (
    sales_by_month
)

from visuals.kpi_card import (
    show_kpi_card
)

from visuals.monthly_sales_chart import (
    render_monthly_sales_chart
)

from visuals.top_account_race import (
    render_chain3_bar_race
)

from business_logic.measures.sales_measures import (

    YTD_OrderValue,
    YTD_LY_OrderValue,
    YTD_YoY_Growth,
    YTD_Trend_13M,
    YTD_OrderValue_Global,
    YTD_LY_OrderValue_Global,
    YTD_YoY_Growth_Global,
    CurrentMonth_OrderValue_Global,
    CurrentMonth_vs_LY_Global,
    CurrentMonth_vs_LastMonth_Global,
    CurrentMonth_vs_Avg3M_Global,
    CurrentMonth_vs_Avg6M_Global
)

from business_logic.cross_filter.pie_cross_filter import (

    initialize_pie_filters,
    apply_pie_filters
)

from visuals.interactive_pie_chart import (
    render_interactive_pie
)

from business_logic.cross_filter.hierarchy_state import (

    initialize_hierarchy_state
)

from visuals.hierarchy_bar_drilldown import (
    render_hierarchy_bar
)

from visuals.hierarchy_sunburst import (
    render_hierarchy_sunburst
)

from visuals.product_flavor_bar_chart import (
    render_product_flavor_bar_chart
)

# =====================================================
# LAYOUT CONFIG
# =====================================================

ROW_HEIGHTS = {

    "R1": 240,
    "R2": 520,
    "R3": 550
}

ROW_GAP = 15

# =====================================================
# PAGE
# =====================================================

def show_overview(
    filtered_df,
    master_df
):

    available_years = sorted(
        filtered_df["order_year"]
        .dropna()
        .unique()
        .tolist()
    )
    # =========================================
    # PIE YEAR
    # =========================================

    pie_year = (
        filtered_df["order_year"]
        .max()
    )

    # =========================================
    # PIE BASE DF
    # =========================================

    pie_base_df = (

        filtered_df[
            filtered_df["order_year"]
            == pie_year
        ]
    )

    # =========================================
    # LOCAL PIE FILTER
    # =========================================

    pie_filtered_df = apply_pie_filters(
        pie_base_df
    )

    # st.write(
    # st.session_state["pie_filters"]
    # )

    # st.write(

    #     "Filtered Rows:",

    #     len(pie_filtered_df)
    # )

    # =================================================
    # ROW 1
    # =================================================
    
    r1_col_1, r1_col_2 = st.columns(2)
    
    # =================================================
    # KPI CALCULATION
    # =================================================

    ytd_value = YTD_OrderValue_Global(
        filtered_df,
        master_df
    )

    ytd_ly_value = YTD_LY_OrderValue_Global(
        filtered_df,
        master_df
    )

    ytd_growth = YTD_YoY_Growth_Global(
        filtered_df,
        master_df
    )
    
    # =================================================
    # TREND
    # =================================================
    
    trend_result = YTD_Trend_13M(
    
        filtered_df,
        master_df
    )
    
    trend_data = (
        trend_result["values"]
    )
    
    trend_categories = (
        trend_result["categories"]
    )
    
    # =========================================
    # INIT HIE STATE
    # =========================================

    initialize_hierarchy_state()


    # =================================================
    # R1-1
    # =================================================
    
    with r1_col_1:
    
        with st.container(
            border=True,
            height=ROW_HEIGHTS["R1"]
        ):
    
            show_kpi_card(
            
                title="Doanh số từ đầu năm đến hiện tại của kênh MT",
    
                value=f"{ytd_value:,.0f}",
    
                unit="VNĐ",
    
                comparisons=[
                
                    {
                        "label": "so với YTD năm trước",
    
                        "value": ytd_growth
                    }
                ],
    
                trend_data=trend_data,
    
                trend_categories=trend_categories,
    
                height="260px"
            )
        
    # =================================================
    # R1-2 KPI
    # =================================================

    current_month_value = (

        CurrentMonth_OrderValue_Global(

            filtered_df,
            master_df
        )
    )

    current_vs_ly = (

        CurrentMonth_vs_LY_Global(

            filtered_df,
            master_df
        )
    )

    current_vs_last_month = (

        CurrentMonth_vs_LastMonth_Global(

            filtered_df,
            master_df
        )
    )

    current_vs_avg3m = (

        CurrentMonth_vs_Avg3M_Global(

            filtered_df,
            master_df
        )
    )

    current_vs_avg6m = (

        CurrentMonth_vs_Avg6M_Global(

            filtered_df,
            master_df
        )
    )
    # =================================================
    # R1-2
    # =================================================
    
    with r1_col_2:
    
        with st.container(
            border=True,
            height=ROW_HEIGHTS["R1"]
        ):
    
            show_kpi_card(
            
                title="Doanh số tháng hiện tại",
    
                value=f"{current_month_value:,.0f}",
    
                unit="VNĐ",
    
                comparisons=[
                
                    {
                        "label": "so với tháng hiện tại năm trước",
                        "value": current_vs_ly
                    },
    
                    {
                        "label": "so với tháng trước",
                        "value": current_vs_last_month
                    },
    
                    {
                        "label": "so với trung bình 3 Tháng gần nhất",
                        "value": current_vs_avg3m
                    },
    
                    {
                        "label": "so với trung bình 6 Tháng gần nhất",
                        "value": current_vs_avg6m
                    }
                ],
    
                trend_data=trend_data,
    
                trend_categories=trend_categories,
    
                height="260px"
            )

    # =================================================
    # ROW GAP
    # =================================================

    st.markdown(
        f"<div style='height:{ROW_GAP}px'></div>",
        unsafe_allow_html=True
    )
    # =================================================
    # ROW 2
    # =================================================

    r2_col_1, r2_col_2 = st.columns([3, 1])

    with r2_col_1:

        with st.container(
            border=True,
            height=ROW_HEIGHTS["R2"]
        ):

            st.subheader(
                "Doanh số bán hàng theo tháng"
            )

            st.divider()

            chart_df = sales_by_month(
                filtered_df
            )

            render_monthly_sales_chart(

                chart_df=chart_df,

                years=available_years,

                unit="VND"
            )

    with r2_col_2:

        with st.container(
            border=True,
            height=ROW_HEIGHTS["R2"]
        ):

            st.subheader(
                "Top Doanh Số Theo Chuỗi"
            )

            st.divider()

            render_chain3_bar_race(

                df=filtered_df,

                unit="VND"
            )

    st.markdown(
        f"<div style='height:{ROW_GAP}px'></div>",
        unsafe_allow_html=True
    )

    # =================================================
    # PIE FILTER ACTION
    # =================================================

    pie_action_col_1, pie_action_col_2 = st.columns(
        [0.85, 0.15]
    )

    with pie_action_col_2:

        if st.button(

            "Clear All",

            use_container_width=True,

            key="clear_all_pie_filter"
        ):

            # =====================================
            # RESET PIE FILTER
            # =====================================

            for key in st.session_state["pie_filters"]:

                st.session_state["pie_filters"][key] = None

            # =====================================
            # RESET EVENT CACHE
            # =====================================

            for key in list(st.session_state.keys()):

                if key.startswith("last_event_"):

                    st.session_state[key] = None

            st.rerun()

    # =================================================
    # ROW 3
    # =================================================

    r3_col_1, r3_col_2 = st.columns(2)

    # =================================================
    # REGION
    # =================================================

    with r3_col_1:

        with st.container(
            border=True,
            height=500
        ):

            render_interactive_pie(

                pie_filtered_df,

                dimension_col="khu_vực",

                title="Doanh số theo Khu vực"
            )

    # =================================================
    # BRAND
    # =================================================

    with r3_col_2:

        with st.container(
            border=True,
            height=500
        ):

            render_interactive_pie(

                pie_filtered_df,

                dimension_col="tbd_brand_1",

                title="Doanh số theo Brand"
            )

    # =================================================
    # ROW 4
    # =================================================

    r4_col_1, r4_col_2 = st.columns(2)

    # =================================================
    # CUSTOMER GROUP
    # =================================================

    with r4_col_1:

        with st.container(
            border=True,
            height=500
        ):

            render_interactive_pie(

                pie_filtered_df,

                dimension_col="nhóm_khách_hàng",

                title="Doanh số theo Nhóm khách hàng"
            )

    # =================================================
    # CHAIN 3
    # =================================================

    with r4_col_2:

        with st.container(
            border=True,
            height=500
        ):

            render_interactive_pie(

                pie_filtered_df,

                dimension_col="chain_3",

                title="Doanh số theo Chuỗi"
            )

    # =================================================
    # SPACE
    # =================================================

    st.markdown(
        f"<div style='height:{ROW_GAP}px'></div>",
        unsafe_allow_html=True
    )

    # =================================================
    # ROW 5
    # =================================================

    r5_col_1, r5_col_2 = st.columns(2)

    # =================================================
    # R5-1
    # =================================================

    with r5_col_1:

        with st.container(
            border=True,
            height=ROW_HEIGHTS["R2"]
        ):

            render_hierarchy_sunburst(
            
                pie_filtered_df,

                title="Doanh số theo Cấu trúc Sản phẩm"
            )

    with r5_col_2:
    
        with st.container(
            border=True,
            height=500
        ):
    
            render_product_flavor_bar_chart(
            
                pie_filtered_df
            )

    # =================================================
    # ROW 3
    # =================================================

    with st.container(
        border=True,
        height=ROW_HEIGHTS["R3"]
    ):

        st.subheader(
            "TF_PurchaseOrder"
        )

        st.divider()

        st.dataframe(
            filtered_df,
            width="stretch",
            height=420
        )