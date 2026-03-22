from typing import List

import chromadb


class ChromaVectorStore:
    def __init__(self, persist_directory: str, collection_name: str):
        self._client = chromadb.PersistentClient(path=persist_directory)
        self._collection = self._client.get_or_create_collection(name=collection_name)

    @property
    def collection(self):
        return self._collection

    def upsert(self, ids, embeddings, documents, metadatas):
        if not ids:
            return

        self._collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def delete(self, ids):
        if not ids:
            return
        self._collection.delete(ids=ids)

    def query(self, embedding, k):
        return self._collection.query(
            query_embeddings=[embedding],
            n_results=k,
            include=["documents", "metadatas", "distances"],
        )

    def get_all(self):
        return self._collection.get(include=["documents", "metadatas"])

    def get_by_ids(self, ids: List[str]):
        if not ids:
            return {"ids": [], "documents": [], "metadatas": []}

        return self._collection.get(
            ids=ids,
            include=["documents", "metadatas"],
        )