from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class SearchResult:
    id: str
    document: str
    metadata: Dict[str, Any]
    score: float