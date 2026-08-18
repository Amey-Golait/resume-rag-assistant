from pathlib import Path

from services.embeddings import generate_embeddings
from services.pdf_extract import extract_text_from_pdf
from services.text_analysis import build_analysis
from services.vectorstore import search_chunks

DEFAULT_COLLECTION = "resumes"


def analyze_resume_against_job(
    resume_filename: str,
    job_description: str,
    persist_dir: Path,
    upload_dir: Path,
    top_k: int = 10,
    model: str | None = None,
) -> dict:
    job_description = job_description.strip()
    if not job_description:
        raise ValueError("job_description is required")

    pdf_path = upload_dir / resume_filename
    if not pdf_path.exists():
        raise FileNotFoundError(f"Resume not found: {resume_filename}")

    resume_text = extract_text_from_pdf(pdf_path)
    if not resume_text.strip():
        raise ValueError("Could not extract text from resume PDF")

    result = build_analysis(resume_text, job_description)
    query_embedding = generate_embeddings([job_description])[0]
    result["sources"] = search_chunks(
        persist_dir,
        query_embedding,
        top_k=top_k,
        collection_name=DEFAULT_COLLECTION,
    )
    result["resume_filename"] = resume_filename

    return result
