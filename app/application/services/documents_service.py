from collections import defaultdict
from typing import Dict, List

from app.domain.models.source_document import SourceDocument
from app.infrastructure.vectorstores.chroma_vector_store import ChromaVectorStore


class DocumentsService:
    def __init__(self, vector_store: ChromaVectorStore):
        self._vector_store = vector_store

    def get_documents_page(self) -> Dict:
        data = self._vector_store.get_all()
        metadatas = data.get("metadatas", [])

        grouped = defaultdict(int)

        for metadata in metadatas:
            if not metadata:
                continue

            source = metadata.get("source", "unknown")
            grouped[source] += 1

        documents = [
            {
                "source": source,
                "chunks": chunks,
            }
            for source, chunks in sorted(grouped.items(), key=lambda item: item[0].lower())
        ]

        return {
            "documents": documents,
            "count": len(documents),
        }