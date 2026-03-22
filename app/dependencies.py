from pathlib import Path

from app.application.services.chat_service import ChatService
from app.application.services.documents_service import DocumentsService
from app.application.services.ingestion_service import IngestionService
from app.application.services.search_service import SearchService
from app.core.config import CHROMA_DIR, COLLECTION_NAME, DOCS_FOLDER, STATE_FILE
from app.core.state import state
from app.infrastructure.embeddings.jina_embedder import JinaEmbedder
from app.infrastructure.llm.ollama_client import OllamaClient
from app.infrastructure.processors.processor_factory import ProcessorFactory
from app.infrastructure.state.json_state_repository import JsonStateRepository
from app.infrastructure.vectorstores.chroma_vector_store import ChromaVectorStore


def get_embedder():
    if state.embed_model is None:
        raise RuntimeError("Embedding model has not been initialized.")
    return JinaEmbedder(state.embed_model)


def get_vector_store():
    return ChromaVectorStore(
        persist_directory=str(CHROMA_DIR),
        collection_name=COLLECTION_NAME,
    )


def get_state_repository():
    return JsonStateRepository(STATE_FILE)


def get_processor_factory():
    return ProcessorFactory()


def get_llm_client():
    return OllamaClient()


def get_ingestion_service():
    return IngestionService(
        docs_folder=Path(DOCS_FOLDER),
        embedder=get_embedder(),
        vector_store=get_vector_store(),
        state_repository=get_state_repository(),
        processor_factory=get_processor_factory(),
    )


def get_search_service():
    return SearchService(
        embedder=get_embedder(),
        vector_store=get_vector_store(),
    )


def get_chat_service():
    return ChatService(
        search_service=get_search_service(),
        llm_client=get_llm_client(),
    )


def get_documents_service():
    return DocumentsService(
        vector_store=get_vector_store(),
    )