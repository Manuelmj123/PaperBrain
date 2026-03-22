from fastapi import APIRouter, Depends

from app.api.schemas.document import DocumentsResponse
from app.application.use_cases.get_documents_page import get_documents_page_use_case
from app.dependencies import get_documents_service

router = APIRouter()


@router.get("/api/documents", response_model=DocumentsResponse)
def get_documents(documents_service=Depends(get_documents_service)):
    result = get_documents_page_use_case(documents_service)
    return DocumentsResponse(**result)