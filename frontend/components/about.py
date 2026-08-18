import streamlit as st


def render_about() -> None:
    st.markdown("## About Project")
    st.markdown(
        """
        **AI Resume Screening & Career Assistant** is a local RAG-powered application
        that helps recruiters and candidates analyze resume fit against job descriptions.

        ### How it works

        1. **Upload** — Resume and job description PDFs are uploaded and parsed.
        2. **Index** — Text is chunked and embedded locally, stored in ChromaDB.
        3. **Analyze** — Local keyword matching compares the resume to the job description.
        4. **Chat** — Ask natural language questions with answers grounded in your documents.

        ### Tech Stack

        | Layer | Technology |
        |-------|------------|
        | Backend | FastAPI, Python |
        | Vector DB | ChromaDB |
        | Embeddings & Analysis | Local Python logic |
        | PDF Parsing | pypdf |
        | Frontend | Streamlit |

        ### Features

        - Resume vs job description match percentage
        - Strengths, weaknesses, and missing skills analysis
        - Resume improvement suggestions
        - Locally generated interview questions
        - RAG chatbot with source citations
        """
    )
