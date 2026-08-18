CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Georgia:wght@700&display=swap');

:root {
    --page-bg: #f7f5ee;
    --paper: #ffffff;
    --paper-soft: #fbfaf6;
    --ink: #2b2520;
    --muted: #71665e;
    --line: #e2ddd2;
    --brand: #7a5548;
    --brand-dark: #5f4036;
    --brand-soft: #efe5df;
    --success-bg: #edf7ed;
    --success-text: #2f6b35;
}

html, body, [class*="css"] {
    font-family: Inter, sans-serif;
    color: var(--ink);
}

.stApp {
    background: var(--page-bg);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2.5rem;
    max-width: 1080px;
}

header[data-testid="stHeader"],
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"] {
    display: none;
}

.hero-container {
    text-align: center;
    padding: 1.75rem 1rem 1.4rem;
    margin: 0 auto 2rem;
    color: var(--ink);
}

.hero-title {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 2.7rem;
    font-weight: 700;
    line-height: 1.1;
    color: var(--brand-dark);
}

.hero-rule {
    width: min(760px, 100%);
    height: 1px;
    background: var(--line);
    margin: 1.15rem auto 1.35rem;
}

.hero-subtitle {
    max-width: 720px;
    margin: 0 auto;
    font-size: 1.05rem;
    color: var(--muted);
}

.upload-card,
.result-card,
.chat-container,
.score-card,
.stat-card,
.app-footer {
    background: var(--paper);
    border: 1px solid var(--line);
    border-radius: 6px;
    box-shadow: 0 2px 8px rgba(62, 45, 35, 0.06);
}

.upload-card {
    padding: 1.4rem;
    min-height: 170px;
}

.upload-card:hover {
    box-shadow: 0 6px 18px rgba(62, 45, 35, 0.1);
}

.upload-card-title,
.result-card-title {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 0.45rem;
}

.upload-card-desc,
.stat-label,
.score-label {
    font-size: 0.9rem;
    color: var(--muted);
}

.success-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--success-bg);
    color: var(--success-text);
    border: 1px solid #cfe6cf;
    border-radius: 4px;
    padding: 0.45rem 0.75rem;
    font-size: 0.86rem;
    font-weight: 600;
    margin-top: 0.75rem;
}

.result-card {
    padding: 1.35rem;
    margin-bottom: 1rem;
}

.result-card-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.8rem;
}

.result-card-icon {
    font-size: 1.25rem;
}

.result-card-body {
    color: #3e362f;
    font-size: 0.95rem;
    line-height: 1.65;
}

.result-card-body ul {
    margin: 0;
    padding-left: 1.25rem;
}

.result-card-body li {
    margin-bottom: 0.5rem;
}

.score-card {
    background: var(--paper-soft);
    padding: 1.8rem;
    text-align: center;
    margin-bottom: 1.5rem;
}

.score-value {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 3.4rem;
    font-weight: 700;
    color: var(--brand);
}

.chat-container {
    padding: 1.35rem;
    margin-top: 1.5rem;
}

.chat-message-user {
    background: var(--brand);
    color: white;
    border-radius: 6px;
    padding: 0.875rem 1.125rem;
    margin: 0.75rem 0;
    max-width: 85%;
    margin-left: auto;
}

.chat-message-assistant {
    background: var(--paper-soft);
    color: var(--ink);
    border: 1px solid var(--line);
    border-radius: 6px;
    padding: 0.875rem 1.125rem;
    margin: 0.75rem 0;
    max-width: 85%;
}

.citation-box {
    background: var(--paper-soft);
    border-left: 4px solid var(--brand);
    border-radius: 0 6px 6px 0;
    padding: 0.75rem 1rem;
    margin-top: 0.75rem;
    font-size: 0.82rem;
    color: var(--muted);
}

.sidebar-brand {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 1.55rem;
    font-weight: 700;
    color: var(--brand-dark);
    margin-bottom: 0.25rem;
}

.sidebar-tagline {
    font-size: 0.78rem;
    color: var(--muted);
    margin-bottom: 1.5rem;
}

.stat-card {
    padding: 1.25rem;
    text-align: center;
}

.stat-value {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--brand);
}

div.stButton > button,
div.stButton > button[kind="primary"],
div.stDownloadButton > button {
    background: var(--brand);
    color: #ffffff;
    border: 1px solid var(--brand-dark);
    border-radius: 4px;
    padding: 0.65rem 1.3rem;
    font-weight: 700;
    transition: background 0.15s ease, transform 0.15s ease;
}

div.stButton > button:hover,
div.stButton > button[kind="primary"]:hover,
div.stDownloadButton > button:hover {
    background: var(--brand-dark);
    color: #ffffff;
    transform: translateY(-1px);
    border-color: var(--brand-dark);
}

div.stButton > button:disabled,
div.stButton > button[kind="primary"]:disabled {
    background: #d8d1c7;
    color: #8a8178;
    border-color: #d8d1c7;
    transform: none;
}

section[data-testid="stSidebar"] {
    background-color: #f1eee6;
    border-right: 1px solid var(--line);
}

section[data-testid="stSidebar"] hr {
    border-color: var(--line);
}

.stProgress > div > div > div > div {
    background: var(--brand);
}

h1, h2, h3 {
    color: var(--ink);
}

h2, h3 {
    font-family: Georgia, "Times New Roman", serif;
}

a {
    color: var(--brand-dark);
}

input,
textarea,
div[data-baseweb="input"],
div[data-baseweb="textarea"] {
    border-radius: 4px;
}

.app-footer {
    margin: 3rem auto 0;
    padding: 1.8rem 1.25rem;
    text-align: center;
}

.app-footer h3 {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 1.05rem;
    margin: 0 0 1rem;
    color: var(--brand-dark);
}

.footer-links {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem 2rem;
    margin-bottom: 1rem;
}

.footer-links a {
    color: var(--ink);
    font-size: 0.9rem;
    text-decoration: none;
}

.footer-links a:hover {
    color: var(--brand);
    text-decoration: underline;
}

.app-footer p {
    margin: 0;
    color: var(--muted);
    font-size: 0.85rem;
}

@media (max-width: 768px) {
    .block-container {
        padding-top: 1rem;
    }

    .hero-title {
        font-size: 2.1rem;
    }

    .footer-links {
        gap: 0.75rem 1rem;
    }
}
</style>
"""
