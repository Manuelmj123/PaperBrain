import logging
from typing import Any, Dict

from app.core.config import TOP_K_DEFAULT
from app.domain.interfaces.llm_client import LlmClient
from app.domain.services.context_builder import build_context
from app.application.services.search_service import SearchService

logger = logging.getLogger("chat_service")


class ChatService:
    def __init__(
        self,
        search_service: SearchService,
        llm_client: LlmClient,
    ):
        self._search_service = search_service
        self._llm_client = llm_client

    def ask(
        self,
        question: str,
        top_k: int = TOP_K_DEFAULT,
    ) -> Dict[str, Any]:
        normalized_question = (question or "").strip()
        effective_top_k = top_k if isinstance(top_k, int) and top_k > 0 else TOP_K_DEFAULT

        logger.info(
            "ChatService.ask started. question=%s top_k=%s",
            normalized_question,
            effective_top_k,
        )

        results = self._search_service.search_documents(
            query=normalized_question,
            top_k=effective_top_k,
        ) or []

        logger.info("Search returned %s results", len(results))

        for index, item in enumerate(results):
            document = getattr(item, "document", None)
            metadata = getattr(item, "metadata", None)
            preview = document[:200] if isinstance(document, str) else document

            logger.info(
                "Result %s -> id=%s document_preview=%s score=%s metadata_type=%s",
                index,
                getattr(item, "id", None),
                preview,
                getattr(item, "score", None),
                type(metadata).__name__,
            )

        context = build_context(results) or ""
        logger.info("Context built successfully. length=%s", len(context))

        answer = self._llm_client.ask(
            question=normalized_question,
            context=context,
        )
        logger.info("LLM answer generated successfully")

        return {
            "answer": answer,
            "sources": [
                {
                    "id": getattr(item, "id", None),
                    "document": getattr(item, "document", None),
                    "metadata": self._make_json_safe(getattr(item, "metadata", None)),
                    "score": getattr(item, "score", None),
                }
                for item in results
            ],
        }

    def _make_json_safe(self, value: Any) -> Any:
        if isinstance(value, dict):
            return {str(key): self._make_json_safe(val) for key, val in value.items()}

        if isinstance(value, list):
            return [self._make_json_safe(item) for item in value]

        if isinstance(value, tuple):
            return [self._make_json_safe(item) for item in value]

        if isinstance(value, (str, int, float, bool)) or value is None:
            return value

        return str(value)