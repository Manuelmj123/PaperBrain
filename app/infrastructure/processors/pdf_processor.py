from io import BytesIO
from pathlib import Path
from typing import List
import logging

import fitz
from PIL import Image, UnidentifiedImageError

from app.core.config import IMAGE_DPI_SCALE
from app.domain.interfaces.document_processor import DocumentProcessor
from app.domain.models.ingest_item import IngestItem
from app.domain.services.chunking_service import chunk_text
from app.shared.utils.id_utils import build_chunk_id


logger = logging.getLogger(__name__)


def _normalize_text(value: str) -> str:
    return " ".join(value.split()).strip()


def render_pdf_page_to_image(page: fitz.Page) -> Image.Image:
    matrix = fitz.Matrix(IMAGE_DPI_SCALE, IMAGE_DPI_SCALE)
    pix = page.get_pixmap(matrix=matrix, alpha=False)

    if pix.width <= 0 or pix.height <= 0:
        raise ValueError("Rendered PDF page has invalid dimensions.")

    try:
        image = Image.open(BytesIO(pix.tobytes("png"))).convert("RGB").copy()
    except UnidentifiedImageError as exc:
        raise ValueError("Failed to decode rendered PDF page image.") from exc

    return image


class PdfProcessor(DocumentProcessor):
    def can_process(self, path: Path) -> bool:
        return path.suffix.lower() == ".pdf"

    def process(
        self,
        path: Path,
        source: str,
        source_hash: str,
    ) -> List[IngestItem]:
        items: List[IngestItem] = []
        chunk_index = 0

        with fitz.open(str(path)) as document:
            total_pages = len(document)

            for page_index in range(total_pages):
                page = document.load_page(page_index)
                page_number = page_index + 1
                page_rect = page.rect

                try:
                    raw_text = page.get_text("text") or ""
                except Exception as exc:
                    logger.warning(
                        "Failed to extract text from PDF page %s for source %s: %s",
                        page_number,
                        source,
                        exc,
                    )
                    raw_text = ""

                text = _normalize_text(raw_text)

                if text:
                    chunks = [chunk.strip() for chunk in chunk_text(text) if chunk and chunk.strip()]

                    for page_chunk_number, chunk in enumerate(chunks):
                        item_id = build_chunk_id(source_hash, chunk_index)

                        items.append(
                            IngestItem(
                                id=item_id,
                                document=chunk,
                                metadata={
                                    "source": source,
                                    "type": "pdf_text",
                                    "page": page_number,
                                    "chunk": chunk_index,
                                    "page_chunk": page_chunk_number,
                                    "total_pages": total_pages,
                                    "page_width": float(page_rect.width),
                                    "page_height": float(page_rect.height),
                                },
                                text=chunk,
                                image=None,
                            )
                        )

                        chunk_index += 1

                try:
                    page_image = render_pdf_page_to_image(page)
                    item_id = build_chunk_id(source_hash, chunk_index)

                    items.append(
                        IngestItem(
                            id=item_id,
                            document=f"PDF page image: {source} page {page_number}",
                            metadata={
                                "source": source,
                                "type": "pdf_image",
                                "page": page_number,
                                "chunk": chunk_index,
                                "total_pages": total_pages,
                                "page_width": float(page_rect.width),
                                "page_height": float(page_rect.height),
                            },
                            text=None,
                            image=page_image,
                        )
                    )

                    chunk_index += 1
                except Exception as exc:
                    logger.warning(
                        "Failed to render PDF page %s as image for source %s: %s",
                        page_number,
                        source,
                        exc,
                    )

        return items