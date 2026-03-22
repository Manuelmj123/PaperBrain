import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"
DOCS_FOLDER = Path(os.getenv("DOCS_FOLDER", str(BASE_DIR / "docs")))

CHROMA_DIR = Path(os.getenv("CHROMA_DIR", str(DATA_DIR / "chroma")))
STATE_FILE = Path(os.getenv("STATE_FILE", str(DATA_DIR / "ingestion_state.json")))

MODEL_NAME = os.getenv("EMBED_MODEL", "jinaai/jina-embeddings-v4")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "documents")

AUTO_INGEST_ON_STARTUP = os.getenv("AUTO_INGEST_ON_STARTUP", "true").lower() == "true"

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

TOP_K_DEFAULT = int(os.getenv("TOP_K", "5"))
TEXT_CHUNK_SIZE = int(os.getenv("TEXT_CHUNK_SIZE", "500"))
TEXT_CHUNK_OVERLAP = int(os.getenv("TEXT_CHUNK_OVERLAP", "100"))
IMAGE_DPI_SCALE = float(os.getenv("IMAGE_DPI_SCALE", "2.0"))