
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

load_dotenv()

# Import your route modules
from app.routes import upload_route, extract_route, query_route, ai_route

# --- Initialize FastAPI App ---
app = FastAPI(
    title="LegalAI Backend",
    version="1.0.0",
    description="Backend service for LegalAI – upload, extract, and process legal documents."
)

# --- Enable CORS (Cross-Origin Resource Sharing) ---
# This allows your React frontend to communicate with your FastAPI backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # You can later restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Register all API routes here ---
app.include_router(upload_route.router)
app.include_router(extract_route.router)
app.include_router(query_route.router)
app.include_router(ai_route.router)

# --- Root route for quick testing ---
@app.get("/")
def home():
    return {
        "message": "Welcome to LegalAI Backend 🚀",
        "endpoints": ["/upload", "/extract_text"],
        "status": "running"
    }