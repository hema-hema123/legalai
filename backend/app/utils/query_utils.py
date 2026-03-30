# app/utils/query_utils.py

import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
INDEX_DIR = "indexes"

def retrieve_top_chunks(index_name: str, question: str, top_k: int = 3):
    """Load FAISS index with robust filename handling."""
    # CRITICAL FIX: Clean the index name exactly like in build_faiss_index
    clean_name = index_name.strip()
    
    index_path = os.path.join(INDEX_DIR, f"{clean_name}.faiss")
    meta_path = os.path.join(INDEX_DIR, f"{clean_name}_meta.pkl")

    print(f"Looking for index: {index_path}")  # DEBUG
    print(f"Looking for meta:  {meta_path}")   # DEBUG

    if not os.path.exists(index_path):
        print(f"Missing FAISS index: {index_path}")
    if not os.path.exists(meta_path):
        print(f"Missing meta file: {meta_path}")

    if not os.path.exists(index_path) or not os.path.exists(meta_path):
        available = os.listdir(INDEX_DIR)
        print(f"Available indexes: {available}")
        raise FileNotFoundError(f"Index or metadata not found for '{clean_name}'")

    # Load index and metadata
    index = faiss.read_index(index_path)
    with open(meta_path, "rb") as f:
        chunks = pickle.load(f)

    # Search
    q_emb = model.encode([question])
    D, I = index.search(np.array(q_emb).astype("float32"), top_k)

    results = []
    for idx, score in zip(I[0], D[0]):
        if 0 <= idx < len(chunks):
            results.append({"chunk": chunks[idx], "score": float(score)})

    return results