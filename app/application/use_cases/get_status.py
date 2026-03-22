from app.core.config import COLLECTION_NAME, MODEL_NAME
from app.core.state import state


def get_status_use_case():
    return {
        "initialized": state.initialized,
        "collection_name": COLLECTION_NAME,
        "embedding_model": MODEL_NAME,
    }