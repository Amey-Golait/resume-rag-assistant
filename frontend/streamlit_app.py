import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))

from api.client import APIClient, APIError
from components.about import render_about
from components.analysis_page import render_analysis_page
from components.chat import render_chat
from components.dashboard import render_dashboard
from components.footer import render_footer
from components.sidebar import render_sidebar
from components.styles import CUSTOM_CSS
from config import APP_TITLE
from state import init_session_state

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
init_session_state()

api = APIClient()

try:
    api.health()
    st.session_state.api_healthy = True
except (APIError, Exception):
    st.session_state.api_healthy = False

page = render_sidebar()

if not st.session_state.api_healthy:
    st.error(
        "Cannot connect to the backend API. Start it with: "
        "`cd app && uvicorn main:app --reload`"
    )

if page == "Dashboard":
    render_dashboard()
elif page == "Resume Analysis":
    render_analysis_page(api)
elif page == "Chat Assistant":
    render_chat(api)
elif page == "About Project":
    render_about()

render_footer()
