from collections import defaultdict
from pathlib import Path
from typing import Dict, List

import logging

from app.domain.interfaces.embedder import Embedder
from app.domain.interfaces.state_repository import StateRepository
from app.domain.models.ingest_item import IngestItem
from app.domain.services.file_discovery_service import (
    list_supported_files,
    relative_source,
)
from app.infrastructure.processors.processor_factory import ProcessorFactory
from app.infrastructure.vectorstores.chroma_vector_store import ChromaVectorStore
from app.shared.utils.hash_utils import hash_file


logger = logging.getLogger("INGESTION")
logging.basicConfig(level=logging.INFO)


class IngestionService:
    def __init__(
        self,
        docs_folder: Path,
        embedder: Embedder,
        vector_store: ChromaVectorStore,
        state_repository: StateRepository,
        processor_factory: ProcessorFactory,
    ):
        self._docs_folder = docs_folder
        self._embedder = embedder
        self._vector_store = vector_store
        self._state_repository = state_repository
        self._processor_factory = processor_factory

    def _group_items(self, items: List[IngestItem]):
        text_items = [item for item in items if item.text is not None]
        image_items = [item for item in items if item.image is not None]

        logger.info(
            f"📦 INGESTION GROUP → text_items={len(text_items)} | image_items={len(image_items)}"
        )

        return text_items, image_items

    def _upsert_text_items(self, items: List[IngestItem]):
        if not items:
            logger.info("⚠️ INGESTION TEXT UPSERT → skipped (no text items)")
            return 0

        logger.info(f"🧠 EMBEDDING TEXT ITEMS → count={len(items)}")

        embeddings = self._embedder.embed_texts([item.text for item in items])

        logger.info("💾 CHROMA UPSERT TEXT ITEMS")

        self._vector_store.upsert(
            ids=[item.id for item in items],
            embeddings=embeddings,
            documents=[item.document for item in items],
            metadatas=[item.metadata for item in items],
        )

        return len(items)

    def _upsert_image_items(self, items: List[IngestItem]):
        if not items:
            logger.info("⚠️ INGESTION IMAGE UPSERT → skipped (no image items)")
            return 0

        logger.info(f"🖼️ EMBEDDING IMAGE ITEMS → count={len(items)}")

        embeddings = self._embedder.embed_images([item.image for item in items])

        logger.info("💾 CHROMA UPSERT IMAGE ITEMS")

        self._vector_store.upsert(
            ids=[item.id for item in items],
            embeddings=embeddings,
            documents=[item.document for item in items],
            metadatas=[item.metadata for item in items],
        )

        return len(items)

    def _build_ingestion_summary(
        self,
        indexed_files: int,
        indexed_chunks: int,
        removed_files: int,
        removed_chunks: int,
        skipped_files: int,
        errors: List[Dict],
    ):
        summary = {
            "indexed_files": indexed_files,
            "indexed_chunks": indexed_chunks,
            "removed_files": removed_files,
            "removed_chunks": removed_chunks,
            "skipped_files": skipped_files,
            "errors": errors,
        }

        logger.info(f"📊 INGESTION SUMMARY → {summary}")

        return summary

    def ingest_documents(self):
        logger.info("🚀 INGESTION STARTED")

        self._docs_folder.mkdir(parents=True, exist_ok=True)

        previous_state = self._state_repository.load()
        logger.info(f"📂 PREVIOUS STATE FILES → {len(previous_state)}")

        current_files = list_supported_files(self._docs_folder)
        logger.info(f"📄 DISCOVERED FILES → {len(current_files)}")

        indexed_files = 0
        indexed_chunks = 0
        skipped_files = 0
        removed_files = 0
        removed_chunks = 0
        errors: List[Dict] = []

        new_state = {}
        current_sources = set()

        for file_path in current_files:
            source = relative_source(self._docs_folder, file_path)
            current_sources.add(source)

            logger.info(f"📄 PROCESSING FILE → {source}")

            try:
                source_hash = hash_file(file_path)
                previous_entry = previous_state.get(source)

                if previous_entry and previous_entry.get("hash") == source_hash:
                    logger.info(f"⏭️ SKIPPED (UNCHANGED HASH) → {source}")
                    new_state[source] = previous_entry
                    skipped_files += 1
                    continue

                if previous_entry and previous_entry.get("ids"):
                    old_ids = previous_entry.get("ids", [])
                    logger.info(f"🗑️ REMOVING OLD CHUNKS → {len(old_ids)}")
                    self._vector_store.delete(old_ids)
                    removed_chunks += len(old_ids)

                logger.info(f"⚙️ RUNNING PROCESSOR FACTORY → {source}")

                items = self._processor_factory.process_file(
                    path=file_path,
                    source=source,
                    source_hash=source_hash,
                )

                logger.info(f"🧩 PROCESSOR OUTPUT ITEMS → {len(items)}")

                text_items, image_items = self._group_items(items)

                indexed_chunks += self._upsert_text_items(text_items)
                indexed_chunks += self._upsert_image_items(image_items)

                new_state[source] = {
                    "hash": source_hash,
                    "ids": [item.id for item in items],
                }

                indexed_files += 1

                logger.info(f"✅ FILE INDEXED SUCCESSFULLY → {source}")

            except Exception as ex:
                logger.error(f"❌ FILE FAILED → {source} → {ex}")

                errors.append(
                    {
                        "source": source,
                        "error": str(ex),
                    }
                )

        removed_sources = set(previous_state.keys()) - current_sources

        for removed_source in removed_sources:
            entry = previous_state.get(removed_source, {})
            ids = entry.get("ids", [])

            logger.info(f"🧹 REMOVED SOURCE DETECTED → {removed_source}")

            if ids:
                logger.info(f"🗑️ DELETING CHUNKS → {len(ids)}")
                self._vector_store.delete(ids)
                removed_chunks += len(ids)

            removed_files += 1

        logger.info("💾 SAVING STATE FILE")

        self._state_repository.save(new_state)

        return self._build_ingestion_summary(
            indexed_files=indexed_files,
            indexed_chunks=indexed_chunks,
            removed_files=removed_files,
            removed_chunks=removed_chunks,
            skipped_files=skipped_files,
            errors=errors,
        )