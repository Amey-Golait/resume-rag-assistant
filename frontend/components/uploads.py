import streamlit as st

from api.client import APIClient, APIError


def _render_success_badge(label: str) -> None:
    st.markdown(
        f'<div class="success-badge">✓ {label}</div>',
        unsafe_allow_html=True,
    )


def render_upload_section(api: APIClient) -> tuple[bool, bool]:
    col_left, col_right = st.columns(2)

    resume_ready = False
    job_ready = False

    with col_left:
        st.markdown(
            """
            <div class="upload-card">
                <div class="upload-card-title">📄 Resume PDF</div>
                <div class="upload-card-desc">
                    Drag and drop or browse to upload the candidate resume.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        resume_file = st.file_uploader(
            "Resume upload",
            type=["pdf"],
            key="resume_uploader",
            label_visibility="collapsed",
            help="Upload a PDF resume",
        )

        if resume_file is not None:
            if st.session_state.resume_upload is None or (
                st.session_state.resume_upload.get("original_filename")
                != resume_file.name
            ):
                with st.spinner("Uploading resume..."):
                    try:
                        result = api.upload_resume(
                            resume_file.getvalue(), resume_file.name
                        )
                        st.session_state.resume_upload = {
                            "filename": result["filename"],
                            "original_filename": result.get(
                                "original_filename", resume_file.name
                            ),
                            "chunks_indexed": result.get("chunks_indexed", 0),
                        }
                        st.session_state.analysis_result = None
                    except APIError as exc:
                        st.error(f"Resume upload failed: {exc}")
                        st.session_state.resume_upload = None

            if st.session_state.resume_upload:
                resume_ready = True
                _render_success_badge(
                    f"{st.session_state.resume_upload['original_filename']} uploaded"
                )

    with col_right:
        st.markdown(
            """
            <div class="upload-card">
                <div class="upload-card-title">📋 Job Description PDF</div>
                <div class="upload-card-desc">
                    Drag and drop or browse to upload the job description.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        job_file = st.file_uploader(
            "Job description upload",
            type=["pdf"],
            key="job_uploader",
            label_visibility="collapsed",
            help="Upload a PDF job description",
        )

        if job_file is not None:
            if st.session_state.job_upload is None or (
                st.session_state.job_upload.get("original_filename") != job_file.name
            ):
                with st.spinner("Uploading job description..."):
                    try:
                        result = api.upload_job(job_file.getvalue(), job_file.name)
                        st.session_state.job_upload = {
                            "filename": result["filename"],
                            "original_filename": result.get(
                                "original_filename", job_file.name
                            ),
                            "text": result.get("text", ""),
                            "chunks_indexed": result.get("chunks_indexed", 0),
                        }
                        st.session_state.job_description_text = result.get("text", "")
                        st.session_state.analysis_result = None
                    except APIError as exc:
                        st.error(f"Job upload failed: {exc}")
                        st.session_state.job_upload = None

            if st.session_state.job_upload:
                job_ready = True
                _render_success_badge(
                    f"{st.session_state.job_upload['original_filename']} uploaded"
                )

    st.markdown("")
    with st.expander("Or paste job description text", expanded=False):
        pasted = st.text_area(
            "Job description",
            value=st.session_state.job_description_text,
            height=150,
            placeholder="Paste the job description here if you don't have a PDF...",
            label_visibility="collapsed",
        )
        if pasted.strip():
            st.session_state.job_description_text = pasted.strip()
            job_ready = True

    return resume_ready, job_ready
