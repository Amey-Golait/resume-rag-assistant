import streamlit as st

from api.client import APIClient, APIError
from components.analysis_results import render_analysis_results
from components.chat import render_chat
from components.hero import render_hero
from components.uploads import render_upload_section


def render_analysis_page(api: APIClient) -> None:
    render_hero()
    resume_ready, job_ready = render_upload_section(api)

    st.markdown("")
    analyze_clicked = st.button(
        "Analyze Resume",
        type="primary",
        disabled=not (resume_ready and job_ready),
        use_container_width=True,
    )

    if not resume_ready or not job_ready:
        st.caption("Upload both a resume and job description to enable analysis.")

    if analyze_clicked:
        resume_filename = st.session_state.resume_upload["filename"]
        job_description = st.session_state.job_description_text

        with st.status("Analyzing resume against job description...", expanded=True) as status:
            st.write("Retrieving document context...")
            st.write("Generating embeddings and searching vector store...")
            st.write("Running AI analysis...")
            try:
                result = api.analyze(resume_filename, job_description)
                st.session_state.analysis_result = result
                status.update(label="Analysis complete!", state="complete")
            except APIError as exc:
                status.update(label="Analysis failed", state="error")
                st.error(str(exc))

    if st.session_state.analysis_result:
        render_analysis_results(st.session_state.analysis_result)

    st.divider()
    render_chat(api, embedded=True)
