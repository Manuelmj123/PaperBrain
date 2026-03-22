from typing import List

from app.core.config import TOP_K_DEFAULT
from app.domain.interfaces.embedder import Embedder
from app.domain.models.search_result import SearchResult
from app.infrastructure.vectorstores.chroma_vector_store import ChromaVectorStore


class SearchService:
    def __init__(
        self,
        embedder: Embedder,
        vector_store: ChromaVectorStore,
    ):
        self._embedder = embedder
        self._vector_store = vector_store

    def search_documents(
        self,
        query: str,
        top_k: int = TOP_K_DEFAULT,
    ) -> List[SearchResult]:
        query_embedding = self._embedder.embed_query(query)

        results = self._vector_store.query(
            embedding=query_embedding,
            k=top_k,
        )

        ids = results.get("ids", [[]])[0]
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        mapped: List[SearchResult] = []

        for item_id, document, metadata, distance in zip(ids, documents, metadatas, distances):
            mapped.append(
                SearchResult(
                    id=item_id,
                    document=document,
                    metadata=metadata or {},
                    score=float(distance),
                )
            )

        return mapped