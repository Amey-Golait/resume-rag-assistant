from pathlib import Path

from services.embeddings import generate_embeddings
from services.text_analysis import extract_relevant_sentences
from services.vectorstore import search_chunks

RESUMES_COLLECTION = "resumes"
JOBS_COLLECTION = "jobs"


def generate_answer(
    question: str,
    persist_dir: Path,
    top_k: int = 5,
    job_description: str | None = None,
    model: str | None = None,
) -> dict:
    query_embedding = generate_embeddings([question])[0]
    resume_matches = search_chunks(
        persist_dir,
        query_embedding,
        top_k=top_k,
        collection_name=RESUMES_COLLECTION,
    )
    job_matches = search_chunks(
        persist_dir,
        query_embedding,
        top_k=top_k,
        collection_name=JOBS_COLLECTION,
    )

    sources = resume_matches + job_matches
    context_chunks = [match["chunk"] for match in sources]
    if job_description and job_description.strip():
        context_chunks.insert(0, job_description.strip())

    if not context_chunks:
        return {
            "answer": "No documents found. Please upload a resume and job description first.",
            "sources": [],
        }

    context = "\n\n".join(context_chunks)
    sentences = extract_relevant_sentences(context, question, limit=4)
    if sentences:
        answer = " ".join(sentences)
    else:
        answer = (
            "I could not find a clear answer in the uploaded documents. "
            "Try asking about a specific skill, project, experience, or requirement."
        )

    return {"answer": answer, "sources": sources}
