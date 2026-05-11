import streamlit as st

from streamlit_echarts import (
    st_echarts,
    JsCode
)

from business_logic.cross_filter.pie_cross_filter import (
    update_pie_filter
)


# =========================================
# INTERACTIVE PIE
# =========================================

def render_interactive_pie(

    df,

    dimension_col,

    title,

    height="420px"
):

    # =====================================
    # CURRENT FILTER
    # =====================================

    current_selected = (
        st.session_state["pie_filters"]
        .get(dimension_col)
    )

    # =====================================
    # GROUP
    # =====================================

    chart_df = (

        df.groupby(
            dimension_col,
            as_index=False
        )["ordervalue"]
        .sum()
        .sort_values(
            "ordervalue",
            ascending=False
        )
        .head(10)
    )
    # =====================================
    # TOTAL
    # =====================================

    total_value = (
        chart_df["ordervalue"]
        .sum()
    )

    # =====================================
    # DATA
    # =====================================

    pie_data = []

    for _, row in chart_df.iterrows():

        is_selected = (
            row[dimension_col]
            == current_selected
        )

        contribution_pct = 0
        
        if total_value != 0:
        
            contribution_pct = (
            
                row["ordervalue"]
                / total_value
            ) * 100
        
        pie_data.append({
        
            "name": row[dimension_col],
        
            "value": round(
                row["ordervalue"],
                0
            ),
        
            "pct": round(
                contribution_pct,
                1
            ),
        
            "selected": is_selected
        })

    # =====================================
    # OPTION
    # =====================================

    option = {

        # =================================
        # TOOLTIP
        # =================================

        "tooltip": {

            "trigger": "item",

                "formatter": JsCode(
                    """
                    function(params) {

                        return (

                            params.name

                            + '<br/><br/>'

                            + 'Doanh số: '

                            + Number(params.value)
                                .toLocaleString('en-US')

                            + ' VNĐ'

                            + '<br/>'

                            + 'Đóng góp: '

                            + params.data.pct

                            + '%'
                        );
                    }
                    """
                )
        },

        # =================================
        # TITLE
        # =================================

        "title": {

            "text": title,

            "left": "center",

            "top": 24,

            "textStyle": {

                "fontSize": 18,

                "fontWeight": 600
            }
        },

        # =================================
        # LEGEND
        # =================================

        "legend": {
        
            "type": "scroll",

            "orient": "horizontal",

            "bottom": 0,

            "left": "center",

            "textStyle": {
            
                "fontSize": 11
            }
        },

        # =================================
        # SERIES
        # =================================

        "series": [

            {

                "type": "pie",

                "radius": [
                    "45%",
                    "72%"
                ],

                "center": [
                    "50%",
                    "52%"
                ],

                "selectedMode": "single",

                "selectedOffset": 12,

                "avoidLabelOverlap": True,

                "animationDuration": 250,

                "animationDurationUpdate": 250,

                "data": pie_data,

                "label": {

                    "formatter": "{b}"
                },

                "itemStyle": {

                    "borderRadius": 8,

                    "borderColor": "#fff",

                    "borderWidth": 2
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

        key=f"pie_{dimension_col}",

        events={

            "click": (
                "function(params) {"
                "return {'clicked': params.data.name};"
                "}"
            )
        }
    )

    # =====================================
    # CLICK VALUE
    # =====================================

    clicked_value = None

    if isinstance(event, dict):

        chart_event = event.get(
            "chart_event"
        )

        if isinstance(chart_event, dict):

            clicked_value = chart_event.get(
                "clicked"
            )

    # =====================================
    # EVENT GUARD
    # =====================================

    session_key = (
        f"last_event_{dimension_col}"
    )

    last_event = (
        st.session_state.get(session_key)
    )

    # =====================================
    # UPDATE FILTER
    # =====================================

    if (

        clicked_value is not None

        and

        clicked_value != last_event
    ):

        # ================================
        # SAVE LAST EVENT
        # ================================

        st.session_state[session_key] = (
            clicked_value
        )

        # ================================
        # RESET ALL PIE FILTER
        # ================================

        for key in st.session_state["pie_filters"]:

            st.session_state["pie_filters"][key] = None

        # ================================
        # APPLY NEW FILTER
        # ================================

        update_pie_filter(

            dimension_col,

            clicked_value
        )

        # ================================
        # SINGLE RERUN
        # ================================

        st.rerun()