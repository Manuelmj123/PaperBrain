from pydantic import BaseModel
from typing import List, Dict, Any


class IngestResponse(BaseModel):
    indexed_files: int
    indexed_chunks: int
    removed_files: int
    removed_chunks: int
    skipped_files: int
    errors: List[Dict[str, Any]]