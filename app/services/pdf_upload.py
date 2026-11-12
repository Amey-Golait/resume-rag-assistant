
import uuid
from io import BytesIO
from pathlib import Path

from fastapi import HTTPException, UploadFile
from pypdf import PdfReader

PDF_MAGIC = b"%PDF"
MAX_PDF_SIZE = 10 * 1024 * 1024  # 10 MB
CHUNK_SIZE = 1024 * 1024  # 1 MB


async def save_pdf(file: UploadFile, upload_dir: Path) -> dict:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    content = bytearray()

    while True:
        chunk = await file.read(CHUNK_SIZE)

        if not chunk:
            break

        if len(content) + len(chunk) > MAX_PDF_SIZE:
            raise HTTPException(
                status_code=413,
                detail="PDF file size must not exceed 10 MB"
            )

        content.extend(chunk)

    if not content.startswith(PDF_MAGIC):
        raise HTTPException(
            status_code=400,
            detail="File is not a valid PDF"
        )

    try:
        PdfReader(BytesIO(content))
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted PDF file"
        ) from exc

    safe_original_name = Path(
        file.filename.replace("\\", "/")
    ).name

    safe_name = f"{uuid.uuid4().hex}_{safe_original_name}"

    upload_dir.mkdir(parents=True, exist_ok=True)

    destination = upload_dir / safe_name
    destination.write_bytes(content)

    return {
        "filename": safe_name,
        "original_filename": safe_original_name,
        "size": len(content),
    }
