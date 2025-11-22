# backend/app/routes/upload_route.py
from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
import time

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a PDF or TXT file → saves with timestamp prefix.
    Returns both original name and the exact saved filename (with timestamp).
    """
    try:
        original_name = file.filename
        ext = original_name.rsplit(".", 1)[-1].lower() if "." in original_name else ""

        # Validate extension
        if ext not in ["pdf", "txt"]:
            raise HTTPException(
                status_code=400,
                detail="Only PDF (.pdf) and TXT (.txt) files are allowed"
            )

        # Create unique filename to prevent overwrites
        timestamp = int(time.time())
        saved_filename = f"{timestamp}_{original_name}"
        file_path = os.path.join(UPLOAD_DIR, saved_filename)

        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "status": "success",
            "original_name": original_name,        # e.g. "Care of hemorrhage.pdf"
            "saved_filename": saved_filename,      # e.g. "1731971234_Care of hemorrhage.pdf" ← this is what you MUST use later
            "path": file_path,
            "message": "File uploaded successfully"
        }

    except Exception as e:
        print(f"Upload error: {e}")  # or use logging
        raise HTTPException(status_code=500, detail="File upload failed on server")