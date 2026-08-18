import streamlit as st

from components.hero import render_hero


def render_dashboard() -> None:
    render_hero()

    col1, col2, col3 = st.columns(3)

    resume = st.session_state.get("resume_upload")
    job = st.session_state.get("job_upload")
    analysis = st.session_state.get("analysis_result")

    with col1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-value">{"✓" if resume else "—"}</div>
                <div class="stat-label">Resume Uploaded</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-value">{"✓" if job or st.session_state.get("job_description_text") else "—"}</div>
                <div class="stat-label">Job Description Ready</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        score = analysis.get("match_percentage", "—") if analysis else "—"
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-value">{f"{score}%" if isinstance(score, int) else score}</div>
                <div class="stat-label">Latest Match Score</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.markdown("### Quick Start")
    st.markdown(
        """
        1. Go to **Resume Analysis** and upload a resume PDF and job description PDF.
        2. Click **Analyze Resume** to get a match score and detailed insights.
        3. Use the **Chat Assistant** to ask follow-up questions with source citations.
        """
    )

    if st.button("Go to Resume Analysis →", type="primary"):
        st.session_state.page = "Resume Analysis"
        st.rerun()
