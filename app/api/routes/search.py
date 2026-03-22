from fastapi import APIRouter, Depends

from app.api.schemas.search import SearchRequest
from app.application.use_cases.search_documents import search_documents_use_case
from app.dependencies import get_search_service

router = APIRouter()


@router.post("/api/search")
def search_documents(
    request: SearchRequest,
    search_service=Depends(get_search_service),
):
    results = search_documents_use_case(
        search_service=search_service,
        query=request.query,
        top_k=request.top_k,
    )

    return {
        "results": [
            {
                "id": item.id,
                "document": item.document,
                "metadata": item.metadata,
                "score": item.score,
            }
            for item in results
        ]
    }