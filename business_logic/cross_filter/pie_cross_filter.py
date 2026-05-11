import streamlit as st


# =========================================
# INIT
# =========================================

def initialize_pie_filters():

    if "pie_filters" not in st.session_state:

        st.session_state["pie_filters"] = {

            "khu_vực": None,
            "tbd_brand_1": None,
            "nhóm_khách_hàng": None,
            "chain_3": None
        }


# =========================================
# UPDATE
# =========================================

def update_pie_filter(

    dimension_col,
    selected_value
):

    current_value = (
        st.session_state["pie_filters"]
        .get(dimension_col)
    )

    # ==============================
    # TOGGLE OFF
    # ==============================

    if current_value == selected_value:

        st.session_state["pie_filters"][dimension_col] = None

    # ==============================
    # TOGGLE ON
    # ==============================

    else:

        st.session_state["pie_filters"][dimension_col] = (
            selected_value
        )


# =========================================
# APPLY LOCAL FILTER
# =========================================

def apply_pie_filters(df):

    filtered_df = df.copy()

    pie_filters = (
        st.session_state["pie_filters"]
    )

    for col, value in pie_filters.items():

        if value is not None:

            filtered_df = filtered_df[

                filtered_df[col] == value
            ]

    return filtered_df