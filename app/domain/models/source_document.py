from dataclasses import dataclass


@dataclass
class SourceDocument:
    source: str
    chunks: int