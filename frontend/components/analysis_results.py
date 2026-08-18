import html

import streamlit as st


def _render_list_card(icon: str, title: str, items: list[str], empty_msg: str) -> None:
    if items:
        body = "<ul>" + "".join(f"<li>{html.escape(item)}</li>" for item in items) + "</ul>"
    else:
        body = f"<p>{html.escape(empty_msg)}</p>"
    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-card-header">
                <span class="result-card-icon">{icon}</span>
                <h3 class="result-card-title">{title}</h3>
            </div>
            <div class="result-card-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_analysis_results(result: dict) -> None:
    score = result.get("match_percentage", 0)
    st.markdown("## Analysis Results")
    st.progress(score / 100)
    st.markdown(
        f"""
        <div class="score-card">
            <div class="score-value">{score}%</div>
            <div class="score-label">Resume Match Score</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if summary := result.get("summary"):
        with st.expander("📊 Detailed Summary", expanded=True):
            st.markdown(
                f"""
                <div class="result-card">
                    <div class="result-card-body">{html.escape(summary)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    col1, col2 = st.columns(2)

    with col1:
        _render_list_card(
            "🎯",
            "Strengths",
            result.get("strengths", []),
            "No strengths identified.",
        )
        _render_list_card(
            "⚠️",
            "Weaknesses",
            result.get("weaknesses", []),
            "No weaknesses identified.",
        )
        _render_list_card(
            "❌",
            "Missing Skills",
            result.get("missing_skills", []),
            "No missing skills identified.",
        )

    with col2:
        _render_list_card(
            "💡",
            "Resume Improvement Suggestions",
            result.get("improvement_suggestions", []),
            "No suggestions available.",
        )
        _render_list_card(
            "🎤",
            "Interview Questions",
            result.get("interview_questions", []),
            "No interview questions generated.",
        )

    sources = result.get("sources", [])
    if sources:
        with st.expander(f"📚 Source Citations ({len(sources)} chunks)", expanded=False):
            for i, source in enumerate(sources, start=1):
                metadata = source.get("metadata", {})
                source_name = metadata.get("source", "Document")
                chunk_index = metadata.get("chunk_index", "?")
                distance = source.get("distance", 0)
                chunk_preview = html.escape(source.get("chunk", "")[:500])
                st.markdown(
                    f"""
                    <div class="citation-box">
                        <strong>Source {i}:</strong> {html.escape(str(source_name))} (chunk {chunk_index})
                        · relevance: {1 - distance:.2f}<br/>
                        {chunk_preview}{"..." if len(source.get("chunk", "")) > 500 else ""}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
