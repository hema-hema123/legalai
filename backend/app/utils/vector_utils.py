import numpy as np
import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer

# Load lightweight embedding model
MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

INDEX_DIR = "indexes"
os.makedirs(INDEX_DIR, exist_ok=True)

def build_faiss_index(chunks: list[str], index_name: str):
    """Create a FAISS index from text chunks and save it."""
    embeddings = model.encode(chunks, show_progress_bar=True)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))

    # Save index
    index_path = os.path.join(INDEX_DIR, f"{index_name}.faiss")
    faiss.write_index(index, index_path)

    # Save chunk metadata
    with open(os.path.join(INDEX_DIR, f"{index_name}_meta.pkl"), "wb") as f:
        pickle.dump(chunks, f)

    return index_path

def load_index(index_name: str):
    """Load FAISS index and metadata."""
    index_path = os.path.join(INDEX_DIR, f"{index_name}.faiss")
    meta_path = os.path.join(INDEX_DIR, f"{index_name}_meta.pkl")
    if not os.path.exists(index_path) or not os.path.exists(meta_path):
        raise FileNotFoundError("Index or metadata not found")
    index = faiss.read_index(index_path)
    with open(meta_path, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

def search_index(index_name: str, query: str, top_k: int = 3):
    """Search FAISS index and return top_k similar chunks."""
    index, chunks = load_index(index_name)
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec).astype("float32"), top_k)
    results = [{"chunk": chunks[i], "score": float(D[0][idx])} for idx, i in enumerate(I[0])]
    return results