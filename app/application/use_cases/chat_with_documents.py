from app.application.services.chat_service import ChatService


def chat_with_documents_use_case(
    chat_service: ChatService,
    question: str,
    top_k: int,
):
    return chat_service.ask(question=question, top_k=top_k)