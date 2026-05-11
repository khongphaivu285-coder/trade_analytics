from streamlit_echarts import (
    st_echarts,
    JsCode
)

import streamlit as st


def render_chain3_bar_race(
    df,
    unit="VNĐ"
):

    # =========================================
    # VIEW MODE
    # =========================================

    view_mode = st.segmented_control(

        "Doanh số theo",

        options=[
            "YTD",
            "Toàn thời gian"
        ],

        default="YTD",

        key="chain3_bar_race_mode"
    )

    # =========================================
    # YTD
    # =========================================

    if view_mode == "YTD":

        max_date = (
            df["orderdate2"]
            .max()
        )

        current_year = (
            max_date.year
        )

        race_df = (

            df[
                (
                    df["order_year"]
                    == current_year
                )

                &

                (
                    df["orderdate2"]
                    <= max_date
                )
            ]
            .groupby(
                "chain_3",
                as_index=False
            )["ordervalue"]
            .sum()
            .sort_values(
                "ordervalue",
                ascending=False
            )
            .head(15)
        )

    # =========================================
    # ALL TIME
    # =========================================

    else:

        race_df = (

            df.groupby(
                "chain_3",
                as_index=False
            )["ordervalue"]
            .sum()
            .sort_values(
                "ordervalue",
                ascending=False
            )
            .head(15)
        )

    # =========================================
    # OPTION
    # =========================================

    option = {

        # =====================================
        # TOOLTIP
        # =====================================

        "tooltip": {

            "trigger": "item",

            "formatter": JsCode(
                """
                function(params) {

                    return (
                        params.name
                        + '<br/>'
                        + Number(params.value).toLocaleString('en-US')
                        + ' VNĐ'
                    );
                }
                """
            )
        },

        # =====================================
        # GRID
        # =====================================

        "grid": {

            "left": "35%",
            "right": "5%",
            "top": "5%",
            "bottom": "5%"
        },

        # =====================================
        # X AXIS
        # =====================================

        "xAxis": {

            "type": "value",

            "show": False
        },

        # =====================================
        # Y AXIS
        # =====================================

        "yAxis": {

            "type": "category",

            "inverse": True,

            "data": (
                race_df["chain_3"]
                .tolist()
            )
        },

        # =====================================
        # SERIES
        # =====================================

        "series": [

            {

                "name": "Tổng DT",

                "type": "bar",

                "data": (
                    race_df["ordervalue"]
                    .round(0)
                    .tolist()
                ),

                "showBackground": True,

                "backgroundStyle": {

                    "borderRadius": [0, 6, 6, 0]
                },

                "itemStyle": {

                    "borderRadius": [0, 6, 6, 0]
                },

                "emphasis": {

                    "focus": "series"
                },

                "label": {

                    "show": False
                }
            }
        ]
    }

    # =========================================
    # RENDER
    # =========================================

    st_echarts(
        options=option,
        height="600px"
    )