import re
from collections import Counter

TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9+#.-]{1,}")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+|\n+")

STOPWORDS = {
    "about",
    "after",
    "also",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "have",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "our",
    "that",
    "the",
    "their",
    "this",
    "to",
    "with",
    "will",
    "you",
    "your",
}

COMMON_SKILLS = {
    "aws",
    "azure",
    "css",
    "docker",
    "django",
    "excel",
    "express",
    "fastapi",
    "figma",
    "flask",
    "git",
    "html",
    "java",
    "javascript",
    "kubernetes",
    "linux",
    "mongodb",
    "mysql",
    "next.js",
    "node",
    "node.js",
    "postgresql",
    "powerbi",
    "python",
    "react",
    "rest",
    "sql",
    "streamlit",
    "tableau",
    "typescript",
}


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def important_terms(text: str, limit: int = 25) -> list[str]:
    counts = Counter(
        token
        for token in tokenize(text)
        if token not in STOPWORDS and len(token) > 2
    )
    skills = [term for term in COMMON_SKILLS if term in counts]
    ranked = [term for term, _ in counts.most_common(limit)]
    return list(dict.fromkeys(skills + ranked))[:limit]


def overlap_terms(resume_text: str, job_description: str) -> tuple[list[str], list[str]]:
    resume_terms = set(important_terms(resume_text, limit=80))
    job_terms = important_terms(job_description, limit=80)
    matched = [term for term in job_terms if term in resume_terms]
    missing = [term for term in job_terms if term not in resume_terms]
    return matched, missing


def estimate_match_percentage(resume_text: str, job_description: str) -> int:
    matched, missing = overlap_terms(resume_text, job_description)
    total = len(matched) + len(missing)
    if total == 0:
        return 0
    return max(0, min(100, round((len(matched) / total) * 100)))


def extract_relevant_sentences(text: str, query: str, limit: int = 3) -> list[str]:
    query_terms = set(important_terms(query, limit=30))
    sentences = [sentence.strip() for sentence in SENTENCE_RE.split(text) if sentence.strip()]
    scored = []

    for sentence in sentences:
        sentence_terms = set(tokenize(sentence))
        score = len(query_terms & sentence_terms)
        if score:
            scored.append((score, len(sentence), sentence))

    scored.sort(key=lambda item: (-item[0], item[1]))
    return [sentence for _, _, sentence in scored[:limit]]


def build_analysis(resume_text: str, job_description: str) -> dict:
    matched, missing = overlap_terms(resume_text, job_description)
    score = estimate_match_percentage(resume_text, job_description)

    strengths = [
        f"Resume includes {term}." for term in matched[:8]
    ] or ["Resume has readable content that can be compared with the job description."]

    weaknesses = [
        f"Job description mentions {term}, but it is not clearly visible in the resume."
        for term in missing[:6]
    ] or ["No major keyword gaps found from the job description."]

    suggestions = [
        f"Add a concrete project, result, or bullet that demonstrates {term}."
        for term in missing[:6]
    ] or ["Make the strongest matching skills easy to find near the top of the resume."]

    questions = [
        f"Can you describe your experience with {term}?"
        for term in matched[:5]
    ]
    questions.extend(
        f"How would you approach learning or applying {term} for this role?"
        for term in missing[:3]
    )

    summary = (
        f"Local analysis found a {score}% keyword match between the resume and job description. "
        f"Matched terms include: {', '.join(matched[:8]) or 'none found'}. "
        f"Main gaps include: {', '.join(missing[:8]) or 'none found'}."
    )

    return {
        "match_percentage": score,
        "summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "missing_skills": missing[:10],
        "improvement_suggestions": suggestions,
        "interview_questions": questions[:8],
    }
