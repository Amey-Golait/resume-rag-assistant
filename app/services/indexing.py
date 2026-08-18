from pathlib import Path

from services.chunking import chunk_text
from services.embeddings import generate_embeddings
from services.pdf_extract import extract_text_from_pdf
from services.vectorstore import store_embeddings

RESUMES_COLLECTION = "resumes"
JOBS_COLLECTION = "jobs"


def index_document(
    pdf_path: Path,
    persist_dir: Path,
    collection_name: str,
) -> dict:
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)

    if not chunks:
        return {
            "source": pdf_path.name,
            "text": text,
            "chunks_indexed": 0,
        }

    embeddings = generate_embeddings(chunks)
    count = store_embeddings(
        persist_dir=persist_dir,
        chunks=chunks,
        embeddings=embeddings,
        source=pdf_path.name,
        collection_name=collection_name,
    )

    return {
        "source": pdf_path.name,
        "text": text,
        "chunks_indexed": count,
    }


def index_resume(pdf_path: Path, persist_dir: Path) -> dict:
    return index_document(pdf_path, persist_dir, RESUMES_COLLECTION)


def index_job_description(pdf_path: Path, persist_dir: Path) -> dict:
    return index_document(pdf_path, persist_dir, JOBS_COLLECTION)
