import streamlit as st

from config import APP_SUBTITLE, APP_TITLE


def render_hero() -> None:
    st.markdown(
        f"""
        <div class="hero-container">
            <div class="hero-title">{APP_TITLE}</div>
            <div class="hero-rule"></div>
            <div class="hero-subtitle">{APP_SUBTITLE}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
