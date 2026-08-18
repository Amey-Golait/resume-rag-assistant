import uuid
from io import BytesIO
from pathlib import Path

from fastapi import HTTPException, UploadFile
from pypdf import PdfReader

PDF_MAGIC = b"%PDF"


async def save_pdf(file: UploadFile, upload_dir: Path) -> dict:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    content = await file.read()
    if not content.startswith(PDF_MAGIC):
        raise HTTPException(status_code=400, detail="File is not a valid PDF")

    try:
        PdfReader(BytesIO(content))
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid or corrupted PDF file") from exc

    safe_name = f"{uuid.uuid4().hex}_{Path(file.filename).name}"
    destination = upload_dir / safe_name
    destination.write_bytes(content)

    return {
        "filename": safe_name,
        "original_filename": file.filename,
        "size": len(content),
    }
