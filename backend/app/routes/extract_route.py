# app/routes/extract_route.py

from fastapi import APIRouter, HTTPException
import os, json, traceback
from app.utils.file_utils import extract_text
from app.utils.chunk_utils import chunk_text
from app.utils.vector_utils import build_faiss_index  # <-- ADD THIS IMPORT

router = APIRouter()
UPLOADS_DIR = "uploads"
PROCESSED_DIR = "processed"
INDEX_DIR = "indexes"
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

def find_latest_file(search_name, uploads_dir=UPLOADS_DIR):
    files = [f for f in os.listdir(uploads_dir) if search_name in f]
    if not files:
        return None
    files.sort(reverse=True)
    return os.path.join(uploads_dir, files[0])

@router.post("/extract_text")
async def extract_text_api(filename: str):
    """
    Extract text → chunk → AND automatically build FAISS index
    """
    try:
        print(f"extract_text_api called, requested filename: {filename}")
        print("Contents of uploads directory:", os.listdir(UPLOADS_DIR))

        # Handle both "Bursitis" and "Bursitis .pdf" cases
        candidate_files = []
        if not filename.endswith(".pdf"):
            candidate_files.append(filename + " .pdf")
        candidate_files.append(filename + ".pdf")
        candidate_files.append(filename)

        file_path = None
        for candidate in candidate_files:
            found = find_latest_file(candidate)
            if found:
                file_path = found
                print(f"Found uploaded file: {file_path}")
                break

        if not file_path:
            raise HTTPException(status_code=404, detail="File not found")

        # Step 1: Extract text
        raw_text = extract_text(file_path)
        if not raw_text or not raw_text.strip():
            raise HTTPException(status_code=400, detail="No text found in file")

        # Step 2: Chunk text
        chunks = chunk_text(raw_text, chunk_size=500, overlap=100)

        # Step 3: Save chunks
        clean_name = filename.split(".")[0].strip()  # "Bursitis"
        output_filename = f"{clean_name}_chunks.json"
        output_path = os.path.join(PROCESSED_DIR, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)

        # Step 4: AUTOMATICALLY BUILD FAISS INDEX
        print(f"Building FAISS index for {clean_name}...")
        index_path = build_faiss_index(chunks, clean_name)  # This saves .faiss + _meta.pkl

        return {
            "status": "success",
            "index_name": clean_name,                    # This is what frontend should use!
            "chunks_created": len(chunks),
            "index_built": True,
            "index_path": index_path,
            "message": f"Document processed and ready for queries! Use index_name: {clean_name}"
        }

    except Exception as e:
        print("Exception in /extract_text:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))