import streamlit as st


# =========================================
# INIT
# =========================================

def initialize_hierarchy_state():

    if "hierarchy_level" not in st.session_state:

        st.session_state["hierarchy_level"] = (
            "brand"
        )

    if "selected_brand" not in st.session_state:

        st.session_state["selected_brand"] = (
            None
        )

    if "selected_line" not in st.session_state:

        st.session_state["selected_line"] = (
            None
        )


# =========================================
# RESET
# =========================================

def reset_hierarchy():

    st.session_state["hierarchy_level"] = (
        "brand"
    )

    st.session_state["selected_brand"] = (
        None
    )

    st.session_state["selected_line"] = (
        None
    )