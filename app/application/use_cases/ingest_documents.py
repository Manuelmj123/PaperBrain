from app.application.services.ingestion_service import IngestionService


def ingest_documents_use_case(ingestion_service: IngestionService):
    return ingestion_service.ingest_documents()