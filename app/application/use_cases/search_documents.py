from app.application.services.search_service import SearchService


def search_documents_use_case(
    search_service: SearchService,
    query: str,
    top_k: int,
):
    return search_service.search_documents(query=query, top_k=top_k)