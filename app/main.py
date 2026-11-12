from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from services.analysis import analyze_resume_against_job
from services.indexing import index_job_description, index_resume
from services.match import match_resume_to_job
from services.pdf_extract import extract_text_from_pdf
from services.pdf_upload import save_pdf
from services.rag import generate_answer

UPLOAD_DIR = Path(__file__).parent / "uploads"
JOB_UPLOAD_DIR = UPLOAD_DIR / "jobs"
VECTORSTORE_DIR = Path(__file__).parent / "vectorstore"

UPLOAD_DIR.mkdir(exist_ok=True)
JOB_UPLOAD_DIR.mkdir(exist_ok=True)
VECTORSTORE_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Resume RAG Assistant")

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)
    job_description: str | None = None


class AnalyzeRequest(BaseModel):
    resume_filename: str = Field(..., min_length=1)
    job_description: str = Field(..., min_length=1)
    top_k: int = Field(default=10, ge=1, le=50)


class MatchRequest(BaseModel):
    job_description: str = Field(..., min_length=1)
    resume_filename: str | None = None
    top_k: int = Field(default=10, ge=1, le=50)


@app.get("/health")
async def health():
    return {"status": "ok"}


async def _upload_pdf(file: UploadFile, upload_dir: Path, index_fn) -> dict:
    result = await save_pdf(file, upload_dir)
    pdf_path = upload_dir / result["filename"]

    try:
        index_result = index_fn(pdf_path, VECTORSTORE_DIR)
        result.update(index_result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return result


@app.post("/upload")
@app.post("/upload/resume")
async def upload_resume(file: UploadFile = File(..., description="PDF resume file")):
    return await _upload_pdf(file, UPLOAD_DIR, index_resume)


@app.post("/upload/job")
async def upload_job_description(
    file: UploadFile = File(..., description="PDF job description file"),
):
    return await _upload_pdf(file, JOB_UPLOAD_DIR, index_job_description)


@app.post("/ask")
async def ask_question(request: AskRequest):
    try:
        return generate_answer(
            question=request.question,
            persist_dir=VECTORSTORE_DIR,
            top_k=request.top_k,
            job_description=request.job_description,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        return analyze_resume_against_job(
            resume_filename=request.resume_filename,
            job_description=request.job_description,
            persist_dir=VECTORSTORE_DIR,
            upload_dir=UPLOAD_DIR,
            top_k=request.top_k,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/match")
async def compare_resume_to_job(request: MatchRequest):
    try:
        return match_resume_to_job(
            job_description=request.job_description,
            persist_dir=VECTORSTORE_DIR,
            upload_dir=UPLOAD_DIR,
            resume_filename=request.resume_filename,
            top_k=request.top_k,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/job-text/{filename}")
async def get_job_text(filename: str):
    pdf_path = JOB_UPLOAD_DIR / filename
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail=f"Job file not found: {filename}")

    try:
        text = extract_text_from_pdf(pdf_path)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Failed to read job PDF") from exc

    return {"filename": filename, "text": text}
