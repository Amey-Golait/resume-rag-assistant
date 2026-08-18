import html

import streamlit as st

from api.client import APIClient, APIError


def _render_message(message: dict) -> None:
    role = message["role"]
    content = message["content"]

    if role == "user":
        st.markdown(
            f'<div class="chat-message-user">{html.escape(content)}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="chat-message-assistant">{html.escape(content)}</div>',
            unsafe_allow_html=True,
        )

        for i, source in enumerate(message.get("sources", []), start=1):
            metadata = source.get("metadata", {})
            source_name = metadata.get("source", "Document")
            chunk = html.escape(source.get("chunk", "")[:300])
            st.markdown(
                f"""
                <div class="citation-box">
                    <strong>Citation {i}</strong> — {html.escape(str(source_name))}<br/>
                    {chunk}{"..." if len(source.get("chunk", "")) > 300 else ""}
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_chat(api: APIClient, embedded: bool = False) -> None:
    if not embedded:
        st.markdown("## Chat Assistant")
        st.caption("Ask questions about the uploaded resume or job description.")

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.info(
            "Start a conversation — try asking about skills, experience, or job fit."
        )
    else:
        for message in st.session_state.chat_history:
            _render_message(message)

    st.markdown("</div>", unsafe_allow_html=True)

    if prompt := st.chat_input("Ask about the resume or job description..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        job_text = st.session_state.get("job_description_text", "")
        with st.spinner("Thinking..."):
            try:
                response = api.ask(prompt, job_description=job_text or None)
                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": response.get("answer", "No answer returned."),
                        "sources": response.get("sources", []),
                    }
                )
            except APIError as exc:
                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": f"Sorry, I encountered an error: {exc}",
                        "sources": [],
                    }
                )

        st.rerun()

    if st.session_state.chat_history and st.button("Clear chat history", type="secondary"):
        st.session_state.chat_history = []
        st.rerun()
