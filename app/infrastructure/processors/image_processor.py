from pathlib import Path
from typing import List

from PIL import Image

from app.core.constants import IMAGE_EXTENSIONS
from app.domain.interfaces.document_processor import DocumentProcessor
from app.domain.models.ingest_item import IngestItem
from app.shared.utils.id_utils import build_chunk_id


class ImageProcessor(DocumentProcessor):
    def can_process(self, path: Path) -> bool:
        return path.suffix.lower() in IMAGE_EXTENSIONS

    def process(
        self,
        path: Path,
        source: str,
        source_hash: str,
    ) -> List[IngestItem]:
        with Image.open(path) as image:
            image = image.convert("RGB").copy()

        item_id = build_chunk_id(source_hash, 0)

        return [
            IngestItem(
                id=item_id,
                document=f"Image file: {source}",
                metadata={
                    "source": source,
                    "type": "image",
                    "chunk": 0,
                },
                text=None,
                image=image,
            )
        ]