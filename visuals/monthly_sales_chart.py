from streamlit_echarts import (
    st_echarts,
    JsCode
)

import streamlit as st


def render_monthly_sales_chart(

    chart_df,
    years,
    unit="VND"
):

    # =========================
    # CHART TYPE TOGGLE
    # =========================

    chart_type = st.segmented_control(

        "Loại biểu đồ",

        options=[
            "Bar",
            "Line"
        ],

        default="Line",

        key="monthly_sales_chart_type"
    )

    # =========================
    # SERIES TYPE
    # =========================

    echart_type = (
        "line"
        if chart_type == "Line"
        else "bar"
    )

    # =========================
    # CURRENT YEAR
    # =========================

    current_year = max(years)

    # =========================
    # BUILD SERIES
    # =========================

    series = []

    for year in years:

        year_df = (
            chart_df[
                chart_df["order_year"] == year
            ]
            .sort_values("order_month")
        )

        # =====================
        # LABEL ONLY CURRENT YEAR
        # =====================

        show_label = (
            year == current_year
        )

        # =====================
        # SERIES CONFIG
        # =====================

        series_config = {

            "name": str(year),

            "type": echart_type,

            "data": (
                year_df["ordervalue"]
                .round(0)
                .tolist()
            ),

            "label": {

                "show": show_label,

                "position": "top",

                "formatter": JsCode(
                    f"""
                    function(params) {{

                        return params.value
                            .toLocaleString('en-US')
                            + ' {unit}';
                    }}
                    """
                )
            }
        }

        # =====================
        # BAR STYLE
        # =====================

        if echart_type == "bar":

            series_config["itemStyle"] = {

                "borderRadius": [4, 4, 0, 0]
            }

        # =====================
        # LINE STYLE
        # =====================

        if echart_type == "line":

            series_config["smooth"] = True

            series_config["symbolSize"] = 8

        series.append(
            series_config
        )

    # =========================
    # X AXIS
    # =========================

    x_axis = (

        chart_df
        .sort_values("order_month")
        ["order_month"]
        .unique()
    )

    x_axis = [

        f"Tháng {month}"

        for month in x_axis
    ]

    # =========================
    # ECHART OPTION
    # =========================

    option = {

        "tooltip": {

            "trigger": "axis"
        },

        "legend": {

            "bottom": 0
        },

        "grid": {

            "left": "3%",
            "right": "3%",
            "top": "10%",
            "bottom": "15%",

            "containLabel": True
        },

        "xAxis": {

            "type": "category",

            "data": x_axis
        },

        "yAxis": {

            "type": "value",

            "name": unit,

            "axisLabel": {

                "formatter": JsCode(
                    """
                    function(value) {

                        return value
                            .toLocaleString('en-US');
                    }
                    """
                )
            }
        },

        "series": series
    }

    # =========================
    # RENDER
    # =========================

    st_echarts(
        options=option,
        height="300px"
    )