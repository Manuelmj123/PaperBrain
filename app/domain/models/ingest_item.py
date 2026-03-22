from dataclasses import dataclass
from typing import Optional, Dict, Any

from PIL.Image import Image as PILImage


@dataclass
class IngestMetadata:
    source: str
    type: str
    page: Optional[int] = None
    chunk: Optional[int] = None


@dataclass
class IngestItem:
    id: str
    document: str
    metadata: Dict[str, Any]
    text: Optional[str] = None
    image: Optional[PILImage] = None