def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    """
    Splits text into overlapping chunks.
    chunk_size = number of characters per chunk
    overlap = how many characters overlap between chunks
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += chunk_size - overlap  # move window forward

    return chunks