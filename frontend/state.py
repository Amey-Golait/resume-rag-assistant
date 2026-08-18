"""Session state initialization and helpers."""

import streamlit as st


def init_session_state() -> None:
    defaults = {
        "page": "Dashboard",
        "chat_history": [],
        "resume_upload": None,
        "job_upload": None,
        "job_description_text": "",
        "analysis_result": None,
        "analysis_running": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_analysis() -> None:
    st.session_state.analysis_result = None
    st.session_state.analysis_running = False
