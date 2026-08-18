import streamlit as st


def render_footer() -> None:
    st.markdown(
        """
        <footer class="app-footer">
            <h3>Developed by Amey Sanjay Golait</h3>
            <div class="footer-links">
                <a href="mailto:ameygolait123@gmail.com">ameygolait123@gmail.com</a>
                <a href="https://github.com/AmeyMindcodes/ai-book-recommender" target="_blank">GitHub</a>
                <a href="https://www.linkedin.com/in/amey-golait-6717402a2" target="_blank">LinkedIn</a>
                <a href="https://www.instagram.com/__amee___/" target="_blank">Instagram</a>
            </div>
            <p>© 2025 ResumeAI - All Rights Reserved</p>
        </footer>
        """,
        unsafe_allow_html=True,
    )
