from pathlib import Path
from typing import List

from app.core.constants import TEXT_EXTENSIONS
from app.domain.interfaces.document_processor import DocumentProcessor
from app.domain.models.ingest_item import IngestItem
from app.domain.services.chunking_service import chunk_text
from app.shared.utils.id_utils import build_chunk_id


def read_text_file(path: Path) -> str:
    encodings = ["utf-8", "utf-8-sig", "latin-1"]

    for encoding in encodings:
        try:
            return path.read_text(encoding=encoding)
        except Exception:
            continue

    return path.read_bytes().decode("utf-8", errors="ignore")


class TextProcessor(DocumentProcessor):
    def can_process(self, path: Path) -> bool:
        return path.suffix.lower() in TEXT_EXTENSIONS

    def process(
        self,
        path: Path,
        source: str,
        source_hash: str,
    ) -> List[IngestItem]:
        text = read_text_file(path).strip()

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
                        "type": "text",
                        "chunk": index,
                    },
                    text=chunk,
                    image=None,
                )
            )

        return items