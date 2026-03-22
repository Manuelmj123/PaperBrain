from typing import List

from app.domain.interfaces.embedder import Embedder


class JinaEmbedder(Embedder):
    def __init__(self, model):
        self._model = model

    def embed_texts(self, texts: List[str]):
        if not texts:
            return []

        embeddings = self._model.encode(texts, task="retrieval")
        return embeddings.tolist() if hasattr(embeddings, "tolist") else embeddings

    def embed_query(self, query: str):
        embedding = self._model.encode([query], task="retrieval")
        if hasattr(embedding, "tolist"):
            embedding = embedding.tolist()
        return embedding[0]

    def embed_images(self, images):
        if not images:
            return []

        embeddings = self._model.encode(images, task="retrieval")
        return embeddings.tolist() if hasattr(embeddings, "tolist") else embeddings