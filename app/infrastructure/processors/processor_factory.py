from pathlib import Path
from typing import List

from app.domain.interfaces.document_processor import DocumentProcessor
from app.domain.models.ingest_item import IngestItem
from app.infrastructure.processors.docx_processor import DocxProcessor
from app.infrastructure.processors.image_processor import ImageProcessor
from app.infrastructure.processors.pdf_processor import PdfProcessor
from app.infrastructure.processors.text_processor import TextProcessor


class ProcessorFactory:
    def __init__(self, processors: List[DocumentProcessor] | None = None):
        self._processors = processors or [
            PdfProcessor(),
            DocxProcessor(),
            TextProcessor(),
            ImageProcessor(),
        ]

    def get_processor(self, path: Path) -> DocumentProcessor:
        for processor in self._processors:
            if processor.can_process(path):
                return processor

        raise ValueError(f"No processor registered for file: {path}")

    def process_file(
        self,
        path: Path,
        source: str,
        source_hash: str,
    ) -> List[IngestItem]:
        processor = self.get_processor(path)
        return processor.process(path=path, source=source, source_hash=source_hash)