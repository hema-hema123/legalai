# backend/app/routes/upload_route.py
from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
import time

# --- Initialize router ---
router = APIRouter()

# --- Upload directory ---
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a PDF or TXT file and save it to the uploads directory.
    Returns file info after saving.
    """
    try:
        filename = file.filename
        ext = filename.split(".")[-1].lower()

        # ✅ Validate file type
        if ext not in ["pdf", "txt"]:
            raise HTTPException(status_code=400, detail="Only PDF or TXT files are allowed")

        # ✅ Create unique filename (avoid overwriting)
        timestamp = int(time.time())
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # ✅ Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "status": "success",
            "filename": unique_filename,
            "path": file_path,
            "message": "File uploaded successfully 🚀"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")