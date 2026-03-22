from fastapi import FastAPI
import threading

from app.api.routes import chat, documents, health, ingest, search, ui
from app.application.services.startup_service import startup_application

app = FastAPI(title="Local Jina + Chroma + Ollama RAG")


app.include_router(ui.router)
app.include_router(health.router)
app.include_router(ingest.router)
app.include_router(documents.router)
app.include_router(search.router)
app.include_router(chat.router)


@app.on_event("startup")
def startup_event():
    threading.Thread(target=startup_application, daemon=True).start()