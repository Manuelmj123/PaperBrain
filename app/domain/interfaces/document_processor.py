from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from app.domain.models.ingest_item import IngestItem


class DocumentProcessor(ABC):

    @abstractmethod
    def can_process(self, path: Path) -> bool:
        pass

    @abstractmethod
    def process(
        self,
        path: Path,
        source: str,
        source_hash: str,
    ) -> List[IngestItem]:
        pass