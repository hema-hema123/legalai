import fitz  # PyMuPDF
import os

def extract_text_from_pdf(file_path: str) -> str:
    """Extracts plain text from a PDF file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text("text")
    return text

def extract_text_from_txt(file_path: str) -> str:
    """Reads plain text from a .txt file."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def extract_text(file_path: str) -> str:
    """Detects file type and calls correct extraction method."""
    ext = file_path.split(".")[-1].lower()
    if ext == "pdf":
        return extract_text_from_pdf(file_path)
    elif ext == "txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError("Unsupported file format")