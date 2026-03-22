from fastapi import APIRouter, Depends

from app.api.schemas.ingest import IngestResponse
from app.application.use_cases.ingest_documents import ingest_documents_use_case
from app.dependencies import get_ingestion_service

router = APIRouter()


@router.post("/api/ingest", response_model=IngestResponse)
def ingest_documents(ingestion_service=Depends(get_ingestion_service)):
    result = ingest_documents_use_case(ingestion_service)
    return IngestResponse(**result)