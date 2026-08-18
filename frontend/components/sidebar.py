import streamlit as st


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown('<p class="sidebar-brand">ResumeAI</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="sidebar-tagline">Local resume screening assistant</p>',
            unsafe_allow_html=True,
        )
        st.divider()

        pages = ["Dashboard", "Resume Analysis", "Chat Assistant", "About Project"]
        page = st.radio(
            "Navigation",
            pages,
            index=pages.index(st.session_state.get("page", "Dashboard")),
            label_visibility="collapsed",
        )
        st.session_state.page = page

        st.divider()
        st.caption("Backend status")
        if st.session_state.get("api_healthy"):
            st.success("API connected", icon="✅")
        else:
            st.warning("API offline", icon="⚠️")

    return page
