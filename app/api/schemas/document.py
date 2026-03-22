from pydantic import BaseModel
from typing import List


class DocumentItemResponse(BaseModel):
    source: str
    chunks: int


class DocumentsResponse(BaseModel):
    documents: List[DocumentItemResponse]
    count: int