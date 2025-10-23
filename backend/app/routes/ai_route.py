from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.query_utils import retrieve_top_chunks
import os

# Optional: choose model library
# Example uses OpenAI API; you can switch to a local model like ctransformers later
from openai import OpenAI

router = APIRouter()

class AIQuery(BaseModel):
    index_name: str
    question: str
    top_k: int = 3

@router.post("/ai_answer")
async def ai_answer(query: AIQuery):
    """
    Retrieve top chunks from FAISS and generate a natural-language answer.
    """
    try:
        # 1️⃣ Retrieve context chunks
        chunks = retrieve_top_chunks(query.index_name, query.question, query.top_k)
        if not chunks:
            raise HTTPException(status_code=404, detail="No relevant chunks found")

        context = "\n\n".join([c["chunk"] for c in chunks])

        # 2️⃣ Query the language model
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        prompt = (
            f"You are a legal assistant. Answer the user's question using the context below.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query.question}\n\n"
            f"Answer:"
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
        )

        answer = response.choices[0].message.content.strip()
        return {"status": "success", "answer": answer, "chunks_used": len(chunks)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))