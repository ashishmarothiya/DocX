from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi import UploadFile
from fastapi import File
from app.services.file_service import save_file
from app.pipelines.document_pipeline import DocumentPipeline
router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    allowed_types = [
        "application/pdf",
        "application/x-pdf",
        "image/jpeg",
        "image/png",
    ]

    ext = Path(file.filename or "").suffix.lower()
    allowed_exts = [".pdf", ".jpeg", ".jpg", ".png"]

    is_valid = (file.content_type in allowed_types) or (ext in allowed_exts)

    if not is_valid:
        raise HTTPException(
            status_code=415,
            detail="Unsupported file type. Only PDF, JPEG, and PNG files are allowed."
        )

    saved_path = await save_file(file)

    pipeline = DocumentPipeline()
    result = await pipeline.process(saved_path)

    return {
        "message": "File uploaded successfully",
        "original_filename": file.filename,
        "saved_path": str(saved_path),
        "pipeline": result
    }

