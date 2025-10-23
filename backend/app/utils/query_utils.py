import pickle, os, faiss, numpy as np
from sentence_transformers import SentenceTransformer

# Load the same embedding model you used during indexing
model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_top_chunks(index_name: str, question: str, top_k: int = 3):
    """Load FAISS index and return top K matching chunks."""
    index_path = f"indexes/{index_name}.faiss"
    meta_path = f"indexes/{index_name}_meta.pkl"

    if not os.path.exists(index_path) or not os.path.exists(meta_path):
        raise FileNotFoundError("Index or metadata not found")

    # Load FAISS index
    index = faiss.read_index(index_path)

    # Load metadata (the stored chunks)
    with open(meta_path, "rb") as f:
        chunks = pickle.load(f)

    # Embed the query
    q_emb = model.encode([question])
    D, I = index.search(np.array(q_emb).astype("float32"), top_k)

    # Collect top chunks
    results = []
    for idx, dist in zip(I[0], D[0]):
        if 0 <= idx < len(chunks):
            results.append({"chunk": chunks[idx], "score": float(dist)})
    return results