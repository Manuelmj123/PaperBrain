from typing import List

from app.domain.models.search_result import SearchResult


MAX_DOCUMENT_CHARS = 1200
MAX_TOTAL_CONTEXT_CHARS = 4000


def build_context(results: List[SearchResult]) -> str:
    parts = []
    total_length = 0

    for item in results or []:
        document = getattr(item, "document", None)
        metadata = getattr(item, "metadata", None) or {}

        if document:
            trimmed_document = document[:MAX_DOCUMENT_CHARS].strip()

            section = f"Source:\n{trimmed_document}"
            parts.append(section)

            total_length += len(section)

        if metadata:
            safe_metadata = {
                k: v
                for k, v in metadata.items()
                if isinstance(v, (str, int, float, bool))
            }

            if safe_metadata:
                section = f"Metadata:\n{safe_metadata}"
                parts.append(section)

                total_length += len(section)

        if total_length >= MAX_TOTAL_CONTEXT_CHARS:
            break

    return "\n\n".join(parts).strip()