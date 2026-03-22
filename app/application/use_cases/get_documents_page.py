from app.application.services.documents_service import DocumentsService


def get_documents_page_use_case(documents_service: DocumentsService):
    return documents_service.get_documents_page()