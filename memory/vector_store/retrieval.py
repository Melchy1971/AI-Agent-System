from memory.vector_store.vector_db import VectorDB


class Retriever:
    """High-level retrieval interface with reranking placeholder."""

    def __init__(self, db: VectorDB):
        self._db = db

    def retrieve(self, query: str, top_k: int = 5) -> list[str]:
        results = self._db.query(query, top_k=top_k)
        return [r["text"] for r in results]
