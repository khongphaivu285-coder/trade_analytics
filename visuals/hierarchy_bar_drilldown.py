import streamlit as st

from streamlit_echarts import (
    st_echarts,
    JsCode
)


# =========================================
# DRILLDOWN BAR
# =========================================

def render_hierarchy_bar(

    df,

    height="650px"
):

    # =====================================
    # STATE
    # =====================================

    level = (
        st.session_state["hierarchy_level"]
    )

    selected_brand = (
        st.session_state["selected_brand"]
    )

    selected_line = (
        st.session_state["selected_line"]
    )

    # =====================================
    # LEVEL 1
    # =====================================

    if level == "brand":

        chart_df = (

            df.groupby(
                "tbd_brand_1",
                as_index=False
            )["ordervalue"]
            .sum()
            .sort_values(
                "ordervalue",
                ascending=False
            )
            .head(15)
        )

        category_col = "tbd_brand_1"

        title = (
            "Brand Hierarchy"
        )

    # =====================================
    # LEVEL 2
    # =====================================

    elif level == "line":

        level_df = (

            df[
                df["tbd_brand_1"]
                == selected_brand
            ]
        )

        chart_df = (

            level_df.groupby(
                "tbd_line_name",
                as_index=False
            )["ordervalue"]
            .sum()
            .sort_values(
                "ordervalue",
                ascending=False
            )
            .head(15)
        )

        category_col = "tbd_line_name"

        title = (
            f"{selected_brand}"
        )

    # =====================================
    # LEVEL 3
    # =====================================

    else:

        level_df = (

            df[
                (
                    df["tbd_brand_1"]
                    == selected_brand
                )

                &

                (
                    df["tbd_line_name"]
                    == selected_line
                )
            ]
        )

        chart_df = (

            level_df.groupby(
                "tbd_flavor",
                as_index=False
            )["ordervalue"]
            .sum()
            .sort_values(
                "ordervalue",
                ascending=False
            )
            .head(15)
        )

        category_col = "tbd_flavor"

        title = (
            f"{selected_line}"
        )

    # =====================================
    # OPTION
    # =====================================

    option = {

        "tooltip": {

            "trigger": "item",

            "formatter": JsCode(
                """
                function(params) {

                    return (

                        params.name

                        + '<br/>'

                        + Number(params.value)
                            .toLocaleString('en-US')

                        + ' VNĐ'
                    );
                }
                """
            )
        },

        "grid": {

            "left": "30%",
            "right": "5%",
            "top": "12%",
            "bottom": "5%"
        },

        "title": {

            "text": title,

            "left": "center"
        },

        "xAxis": {

            "type": "value",

            "show": False
        },

        "yAxis": {

            "type": "category",

            "inverse": True,

            "data": (
                chart_df[category_col]
                .tolist()
            )
        },

        "series": [

            {

                "type": "bar",

                "data": (
                    chart_df["ordervalue"]
                    .round(0)
                    .tolist()
                ),

                "barWidth": 28,

                "label": {

                    "show": False
                },

                "itemStyle": {

                    "borderRadius": [
                        0,
                        6,
                        6,
                        0
                    ]
                }
            }
        ]
    }

    # =====================================
    # EVENT
    # =====================================

    event = st_echarts(

        options=option,

        height=height,

        key="hierarchy_bar",

        events={

            "click": (
                "function(params) {"
                "return {'clicked': params.name};"
                "}"
            )
        }
    )

    # =====================================
    # EVENT VALUE
    # =====================================

    clicked_value = None

    if isinstance(event, dict):

        chart_event = (
            event.get("chart_event")
        )

        if isinstance(chart_event, dict):

            clicked_value = (
                chart_event.get("clicked")
            )

    # =====================================
    # DRILLDOWN
    # =====================================

    if clicked_value is not None:

        # ================================
        # BRAND → LINE
        # ================================

        if level == "brand":

            st.session_state[
                "selected_brand"
            ] = clicked_value

            st.session_state[
                "hierarchy_level"
            ] = "line"

            st.rerun()

        # ================================
        # LINE → FLAVOR
        # ================================

        elif level == "line":

            st.session_state[
                "selected_line"
            ] = clicked_value

            st.session_state[
                "hierarchy_level"
            ] = "flavor"

            st.rerun()

    # =====================================
    # BACK BUTTON
    # =====================================

    back_col_1, back_col_2 = st.columns(
        [0.2, 0.8]
    )

    with back_col_1:

        if level != "brand":

            if st.button(
                "← Back",
                use_container_width=True
            ):

                # =========================
                # FLAVOR → LINE
                # =========================

                if level == "flavor":

                    st.session_state[
                        "hierarchy_level"
                    ] = "line"

                    st.session_state[
                        "selected_line"
                    ] = None

                # =========================
                # LINE → BRAND
                # =========================

                else:

                    st.session_state[
                        "hierarchy_level"
                    ] = "brand"

                    st.session_state[
                        "selected_brand"
                    ] = None

                st.rerun()