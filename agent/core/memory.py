from __future__ import annotations
from typing import Any


class MemoryManager:
    """Unified interface over short-term buffer, long-term store, and vector memory."""

    def __init__(self):
        self._short_term: list[dict[str, Any]] = []
        # Long-term and vector backends are injected via dependency injection.
        self._long_term = None
        self._vector = None

    def add(self, entry: dict[str, Any]) -> None:
        self._short_term.append(entry)

    def recent(self, n: int = 10) -> list[dict[str, Any]]:
        return self._short_term[-n:]

    def clear_short_term(self) -> None:
        self._short_term.clear()

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """Semantic search over vector memory. Returns empty list if not configured."""
        if self._vector is None:
            return []
        return self._vector.query(query, top_k=top_k)

    def persist(self, key: str, value: Any) -> None:
        if self._long_term is not None:
            self._long_term.set(key, value)

    def recall(self, key: str) -> Any | None:
        if self._long_term is None:
            return None
        return self._long_term.get(key)
