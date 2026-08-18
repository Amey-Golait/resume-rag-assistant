def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    text = text.strip()
    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap must be non-negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: list[str] = []
    start = 0

    while start < len(text):
        chunk = text[start : start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)

        if start + chunk_size >= len(text):
            break

        start += chunk_size - overlap

    return chunks
