import json
import logging
from typing import Optional

import requests

from app.core.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.domain.interfaces.llm_client import LlmClient

logger = logging.getLogger("ollama_client")


class OllamaClient(LlmClient):
    def __init__(
        self,
        base_url: str = OLLAMA_BASE_URL,
        model: str = OLLAMA_MODEL,
        timeout: int = 900,
        connect_timeout: int = 10,
        max_context_chars: int = 3000,
    ):
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._timeout = timeout
        self._connect_timeout = connect_timeout
        self._max_context_chars = max_context_chars
        self._session = requests.Session()

    def ask(self, question: str, context: str) -> str:
        normalized_question = (question or "").strip()
        normalized_context = self._normalize_context(context)

        if not normalized_question:
            return "No question was provided."

        if not normalized_context:
            return "I could not find anything relevant in the indexed documents."

        prompt = self._build_prompt(
            question=normalized_question,
            context=normalized_context,
        )

        try:
            logger.info("Sending request to Ollama model=%s", self._model)

            response = self._session.post(
                f"{self._base_url}/api/generate",
                json={
                    "model": self._model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=(self._connect_timeout, self._timeout),
            )

            logger.info("Received response from Ollama status=%s", response.status_code)
            response.raise_for_status()

        except requests.exceptions.ConnectTimeout:
            logger.exception("Timed out connecting to Ollama at %s", self._base_url)
            return "The local Ollama service took too long to accept the connection."
        except requests.exceptions.ReadTimeout:
            logger.exception("Ollama generation timed out for model %s", self._model)
            return "The local model took too long to respond. Try a shorter question, reduce the retrieved context, or use a smaller model."
        except requests.exceptions.ConnectionError:
            logger.exception("Could not connect to Ollama at %s", self._base_url)
            return "Could not connect to the local Ollama service. Make sure the Ollama container is running and reachable."
        except requests.exceptions.HTTPError as ex:
            status_code = ex.response.status_code if ex.response is not None else "unknown"
            response_text = ex.response.text[:2000] if ex.response is not None and ex.response.text else ""
            logger.exception(
                "Ollama returned HTTP %s for model %s. Response: %s",
                status_code,
                self._model,
                response_text,
            )
            return f"Ollama returned an HTTP {status_code} error while generating the response."
        except requests.exceptions.RequestException:
            logger.exception("Unexpected request error while calling Ollama")
            return "An unexpected network error occurred while contacting the local Ollama service."

        raw_text = (response.text or "").strip()
        if not raw_text:
            logger.error("Ollama returned an empty response body")
            return "The local Ollama service returned an empty response."

        try:
            data = response.json()
            answer = self._extract_answer(data)
            if answer:
                return answer

            logger.warning("Ollama JSON response did not contain a usable answer: %s", data)
            return "The local model did not return a usable answer."

        except ValueError:
            logger.warning("Ollama response was not a single JSON object. Attempting to parse as JSON lines.")
            logger.debug("Raw Ollama response: %s", raw_text[:4000])

            answer = self._parse_json_lines_response(raw_text)
            if answer:
                return answer

            logger.error("Could not parse Ollama response. Raw response: %s", raw_text[:4000])
            return "The local Ollama service returned an invalid response."

    def _build_prompt(self, question: str, context: str) -> str:
        return (
            "You are a helpful assistant answering questions only from the provided context.\n"
            "Use only the facts that appear in the context.\n"
            "If the answer is not in the context, say you could not find it in the indexed documents.\n"
            "When the context contains counts, totals, statuses, locations, or batch information, answer carefully and do not invent values.\n\n"
            f"Context:\n{context}\n\n"
            f"Question:\n{question}\n\n"
            "Answer:"
        )

    def _normalize_context(self, context: Optional[str]) -> str:
        cleaned = (context or "").strip()
        if not cleaned:
            return ""

        if len(cleaned) <= self._max_context_chars:
            return cleaned

        logger.info(
            "Trimming context from %s to %s characters before sending to Ollama",
            len(cleaned),
            self._max_context_chars,
        )
        return cleaned[: self._max_context_chars]

    def _extract_answer(self, data: dict) -> str:
        response_text = data.get("response")
        if isinstance(response_text, str) and response_text.strip():
            return response_text.strip()

        message = data.get("message")
        if isinstance(message, dict):
            content = message.get("content")
            if isinstance(content, str) and content.strip():
                return content.strip()

        return ""

    def _parse_json_lines_response(self, raw_text: str) -> str:
        parts = []

        for line in raw_text.splitlines():
            line = line.strip()
            if not line:
                continue

            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue

            response_piece = item.get("response")
            if isinstance(response_piece, str):
                parts.append(response_piece)

        return "".join(parts).strip()