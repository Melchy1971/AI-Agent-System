from typing import Any


class VectorDB:
    """ChromaDB-backed vector store for semantic memory retrieval."""

    def __init__(self, collection: str = "agent_memory", persist_dir: str = "storage/vector_index"):
        import chromadb
        self._client = chromadb.PersistentClient(path=persist_dir)
        self._col = self._client.get_or_create_collection(collection)

    def add(self, doc_id: str, text: str, metadata: dict[str, Any] | None = None) -> None:
        self._col.add(documents=[text], ids=[doc_id], metadatas=[metadata or {}])

    def query(self, text: str, top_k: int = 5) -> list[dict[str, Any]]:
        results = self._col.query(query_texts=[text], n_results=top_k)
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        return [{"text": d, "metadata": m} for d, m in zip(docs, metas)]

    def delete(self, doc_id: str) -> None:
        self._col.delete(ids=[doc_id])
