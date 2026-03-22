from typing import List
from app.core.config import (
    TEXT_CHUNK_SIZE,
    TEXT_CHUNK_OVERLAP,
)


def chunk_text(text: str) -> List[str]:

    chunks = []

    start = 0
    length = len(text)

    while start < length:

        end = start + TEXT_CHUNK_SIZE

        chunks.append(text[start:end])

        start += TEXT_CHUNK_SIZE - TEXT_CHUNK_OVERLAP

    return chunks