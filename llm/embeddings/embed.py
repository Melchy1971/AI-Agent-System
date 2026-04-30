from typing import Any


class Embedder:
    """Wraps sentence-transformers for local embedding or OpenAI for remote."""

    def __init__(self, model: str = "all-MiniLM-L6-v2", provider: str = "local"):
        self._provider = provider
        self._model_name = model
        self._model = None

    def _load(self):
        if self._model is None:
            if self._provider == "local":
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self._model_name)
            else:
                raise ValueError(f"Unknown embedding provider: {self._provider!r}")

    def embed(self, text: str) -> list[float]:
        self._load()
        return self._model.encode(text).tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        self._load()
        return self._model.encode(texts).tolist()
