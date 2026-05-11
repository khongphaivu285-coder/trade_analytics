from streamlit_echarts import (
    st_echarts,
    JsCode
)

import streamlit as st


def show_kpi_card(

    title,
    value,

    unit=None,

    comparisons=None,

    trend_data=None,

    trend_categories=None,

    height="220px"
):

    # =====================================
    # DEFAULT
    # =====================================

    if comparisons is None:

        comparisons = []

    if trend_data is None:

        trend_data = []

    if trend_categories is None:

        trend_categories = list(
            range(len(trend_data))
        )

    # =====================================
    # COLOR
    # =====================================

    positive = True

    if len(comparisons) > 0:

        positive = (
            comparisons[0]["value"] >= 0
        )

    trend_color = (
        "#21C354"
        if positive
        else "#FF4B4B"
    )

    area_color = (
        "rgba(33,195,84,0.10)"
        if positive
        else "rgba(255,75,75,0.10)"
    )

    # =====================================
    # LAYOUT
    # =====================================

    left_col, right_col = st.columns(
        [1.2, 1]
    )

    # =====================================
    # LEFT
    # =====================================

    with left_col:

        # TITLE
        st.markdown(

            f"""
            <div style="
                font-size:16px;
                color:#4B5563;
                font-weight:500;
                margin-bottom:8px;
            ">
                {title}
            </div>
            """,

            unsafe_allow_html=True
        )

        # VALUE
        st.markdown(

            f"""
            <div style="
                font-size:42px;
                font-weight:700;
                color:#111827;
                line-height:1.1;
                margin-bottom:4px;
            ">
                {value}
            </div>
            """,

            unsafe_allow_html=True
        )

        # UNIT
        if unit:

            st.markdown(

                f"""
                <div style="
                    font-size:12px;
                    color:#9CA3AF;
                    margin-bottom:18px;
                ">
                    {unit}
                </div>
                """,

                unsafe_allow_html=True
            )

            # COMPARISON
            if len(comparisons) > 0:
            
                for compare in comparisons:
                
                    compare_value = compare["value"]

                    positive = (
                        compare_value >= 0
                    )

                    compare_color = (
                        "#21C354"
                        if positive
                        else "#FF4B4B"
                    )

                    bg_color = (
                        "rgba(33,195,84,0.12)"
                        if positive
                        else "rgba(255,75,75,0.12)"
                    )

                    icon = (
                        "↑"
                        if positive
                        else "↓"
                    )

                    compare_text = (
                        f"+{compare_value:,.1f}%"
                        if positive
                        else f"{compare_value:,.1f}%"
                    )

                    compare_label = compare["label"]

                    # =============================
                    # SINGLE CHIP
                    # =============================

                    st.markdown(
                    
                        f"""
                        <span style='background:{bg_color}; padding:8px 16px; border-radius:999px; display:inline-block; margin-bottom:14px;'>

                        <span style='color:{compare_color}; font-size:14px; font-weight:700;'>
                        {icon} {compare_text}
                        </span>

                        <span style='color:#6B7280; font-size:14px; margin-left:12px;'>
                        {compare_label}
                        </span>

                        </span>
                        """,

                        unsafe_allow_html=True
                    )
    # =====================================
    # RIGHT
    # =====================================

    with right_col:

        option = {

            "animation": False,

            # =================================
            # TOOLTIP
            # =================================

            "tooltip": {

                "trigger": "axis",

                "formatter": JsCode(
                    """
                    function(params) {

                        let p = params[0];

                        return (

                            p.axisValue

                            + '<br/>'

                            + Number(p.value)
                                .toLocaleString('en-US')

                            + ' VNĐ'
                        );
                    }
                    """
                )
            },

            # =================================
            # GRID
            # =================================

            "grid": {

                "left": 0,
                "right": 0,
                "top": 15,
                "bottom": 15
            },

            # =================================
            # X AXIS
            # =================================

            "xAxis": {

                "type": "category",

                "show": False,

                "boundaryGap": False,

                "data": trend_categories
            },

            # =================================
            # Y AXIS
            # =================================

            "yAxis": {

                "type": "value",

                "show": False,

                "scale": True
            },

            # =================================
            # SERIES
            # =================================

            "series": [

                {

                    "type": "line",

                    "smooth": True,

                    "symbol": "circle",

                    "symbolSize": 6,

                    "data": trend_data,

                    "lineStyle": {

                        "width": 3,

                        "color": trend_color
                    },

                    "itemStyle": {

                        "color": trend_color
                    },

                    "areaStyle": {

                        "opacity": 1,

                        "color": area_color
                    }
                }
            ]
        }

        st_echarts(

            options=option,

            height="180px",

            key=f"kpi_{title}"
        )