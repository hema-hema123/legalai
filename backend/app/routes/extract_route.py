from fastapi import APIRouter, HTTPException
import os, json
from app.utils.file_utils import extract_text
from app.utils.chunk_utils import chunk_text

router = APIRouter()

PROCESSED_DIR = "processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

@router.post("/extract_text")
async def extract_text_api(filename: str):
    """
    Given a filename from uploads/, extract and chunk the text.
    Saves chunks to processed/ as a JSON file.
    """
    try:
        file_path = os.path.join("uploads", filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found in uploads folder")

        # ✅ Step 1: Extract text
        raw_text = extract_text(file_path)
        if not raw_text.strip():
            raise HTTPException(status_code=400, detail="No text found in file")

        # ✅ Step 2: Chunk text
        chunks = chunk_text(raw_text, chunk_size=500, overlap=100)

        # ✅ Step 3: Save chunks to processed folder
        output_filename = filename.split(".")[0] + "_chunks.json"
        output_path = os.path.join(PROCESSED_DIR, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)

        return {
            "status": "success",
            "chunks_created": len(chunks),
            "output_file": output_filename,
            "message": "Text extracted and chunked successfully 🚀"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))