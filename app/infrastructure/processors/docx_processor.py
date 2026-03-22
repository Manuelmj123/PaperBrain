from pathlib import Path
from typing import List

from docx import Document

from app.core.constants import DOCX_EXTENSIONS
from app.domain.interfaces.document_processor import DocumentProcessor
from app.domain.models.ingest_item import IngestItem
from app.domain.services.chunking_service import chunk_text
from app.shared.utils.id_utils import build_chunk_id


def read_docx_file(path: Path) -> str:
    document = Document(str(path))
    parts = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:
            parts.append(text)

    return "\n".join(parts)


class DocxProcessor(DocumentProcessor):
    def can_process(self, path: Path) -> bool:
        return path.suffix.lower() in DOCX_EXTENSIONS

    def process(
        self,
        path: Path,
        source: str,
        source_hash: str,
    ) -> List[IngestItem]:
        text = read_docx_file(path).strip()

        if not text:
            return []

        chunks = chunk_text(text)
        items: List[IngestItem] = []

        for index, chunk in enumerate(chunks):
            item_id = build_chunk_id(source_hash, index)

            items.append(
                IngestItem(
                    id=item_id,
                    document=chunk,
                    metadata={
                        "source": source,
                        "type": "docx",
                        "chunk": index,
                    },
                    text=chunk,
                    image=None,
                )
            )

        return items