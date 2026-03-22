from abc import ABC, abstractmethod
from typing import List


class Embedder(ABC):

    @abstractmethod
    def embed_texts(self, texts: List[str]):
        pass

    @abstractmethod
    def embed_query(self, query: str):
        pass

    @abstractmethod
    def embed_images(self, images):
        pass