from fastapi import APIRouter, HTTPException
import os, json
from app.utils.vector_utils import build_faiss_index, search_index

router = APIRouter()

@router.post("/build_index")
async def build_index_api(processed_file: str):
    """
    Build a FAISS index from a processed chunks JSON file.
    processed_file should exist in /processed folder.
    """
    try:
        file_path = os.path.join("processed", processed_file)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Processed file not found")

        with open(file_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)

        base_name = processed_file.replace("_chunks.json", "")
        index_path = build_faiss_index(chunks, base_name)

        return {"status": "success", "index_path": index_path, "message": "FAISS index built successfully 🚀"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query")
async def query_index_api(index_name: str, question: str, top_k: int = 3):
    """
    Search within an existing FAISS index for the most relevant chunks.
    """
    try:
        results = search_index(index_name, question, top_k=top_k)
        return {"status": "success", "results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))