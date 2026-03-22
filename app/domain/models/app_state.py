from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class AppState:
    embed_model: Optional[Any] = None
    chroma_client: Optional[Any] = None
    collection: Optional[Any] = None
    initialized: bool = False


state = AppState()