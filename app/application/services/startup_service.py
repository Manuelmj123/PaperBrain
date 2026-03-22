from pathlib import Path
import time
import logging

from app.core.config import (
    AUTO_INGEST_ON_STARTUP,
    CHROMA_DIR,
    COLLECTION_NAME,
    DATA_DIR,
    DOCS_FOLDER,
    MODEL_NAME,
    STATE_FILE,
)
from app.core.state import state
from app.application.services.ingestion_service import IngestionService
from app.infrastructure.embeddings.jina_embedder import JinaEmbedder
from app.infrastructure.processors.processor_factory import ProcessorFactory
from app.infrastructure.state.json_state_repository import JsonStateRepository
from app.infrastructure.vectorstores.chroma_vector_store import ChromaVectorStore


logger = logging.getLogger("startup")
logging.basicConfig(level=logging.INFO)


def startup_application():
    logger.info("STARTUP: begin")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"STARTUP: DATA_DIR ready -> {DATA_DIR}")

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"STARTUP: CHROMA_DIR ready -> {CHROMA_DIR}")

    DOCS_FOLDER.mkdir(parents=True, exist_ok=True)
    logger.info(f"STARTUP: DOCS_FOLDER ready -> {DOCS_FOLDER}")

    if state.initialized:
        logger.info("STARTUP: already initialized — skipping")
        return

    logger.info("STARTUP: importing SentenceTransformer")

    from sentence_transformers import SentenceTransformer

    start = time.time()

    logger.info(f"STARTUP: loading embedding model -> {MODEL_NAME}")

    model = SentenceTransformer(
        MODEL_NAME,
        trust_remote_code=True,
    )

    logger.info(
        f"STARTUP: embedding model loaded in {round(time.time() - start, 2)} seconds"
    )

    embedder = JinaEmbedder(model)
    logger.info("STARTUP: embedder initialized")

    logger.info("STARTUP: initializing ChromaVectorStore")

    vector_store = ChromaVectorStore(
        persist_directory=str(CHROMA_DIR),
        collection_name=COLLECTION_NAME,
    )

    logger.info("STARTUP: vector store initialized")

    state_repository = JsonStateRepository(STATE_FILE)
    logger.info(f"STARTUP: state repository ready -> {STATE_FILE}")

    processor_factory = ProcessorFactory()
    logger.info("STARTUP: processor factory initialized")

    state.embed_model = model
    state.chroma_client = getattr(vector_store, "_client", None)
    state.collection = vector_store.collection
    state.initialized = True

    logger.info("STARTUP: global state initialized")
    
    if AUTO_INGEST_ON_STARTUP:
        logger.info("STARTUP: AUTO_INGEST_ON_STARTUP enabled — running ingestion")

        ingestion_service = IngestionService(
            docs_folder=Path(DOCS_FOLDER),
            embedder=embedder,
            vector_store=vector_store,
            state_repository=state_repository,
            processor_factory=processor_factory,
        )

        result = ingestion_service.ingest_documents()

        logger.info(f"STARTUP: ingestion completed -> {result}")

    else:
        logger.info("STARTUP: AUTO_INGEST_ON_STARTUP disabled — skipping ingestion")

    logger.info("STARTUP: complete")