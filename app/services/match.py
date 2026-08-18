from pathlib import Path

from services.embeddings import generate_embeddings
from services.pdf_extract import extract_text_from_pdf
from services.text_analysis import build_analysis
from services.vectorstore import search_chunks


def match_resume_to_job(
    job_description: str,
    persist_dir: Path,
    upload_dir: Path,
    resume_filename: str | None = None,
    top_k: int = 10,
    model: str | None = None,
) -> dict:
    job_description = job_description.strip()
    if not job_description:
        raise ValueError("job_description is required")

    matches = []
    if resume_filename:
        pdf_path = upload_dir / resume_filename
        if not pdf_path.exists():
            raise FileNotFoundError(f"Resume not found: {resume_filename}")
        resume_context = extract_text_from_pdf(pdf_path)
    else:
        query_embedding = generate_embeddings([job_description])[0]
        matches = search_chunks(persist_dir, query_embedding, top_k=top_k)
        if not matches:
            return {
                "match_percentage": 0,
                "summary": "No resume data found. Please upload a resume first.",
                "strengths": [],
                "gaps": [],
                "sources": [],
            }
        resume_context = "\n\n".join(match["chunk"] for match in matches)

    result = build_analysis(resume_context, job_description)
    result["gaps"] = result.get("missing_skills", [])

    if not resume_filename:
        result["sources"] = matches
    else:
        result["resume_filename"] = resume_filename

    return result
