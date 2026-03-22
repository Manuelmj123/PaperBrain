from abc import ABC, abstractmethod
from typing import List


class VectorStore(ABC):

    @abstractmethod
    def upsert(self, ids, embeddings, documents, metadatas):
        pass

    @abstractmethod
    def delete(self, ids):
        pass

    @abstractmethod
    def query(self, embedding, k):
        pass

    @abstractmethod
    def get_all(self):
        pass