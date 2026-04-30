#!/usr/bin/env python3
"""Seed the vector store with initial knowledge."""
from memory.vector_store.vector_db import VectorDB

SEED_DOCS = [
    ("doc_1", "The agent system uses a plan-execute-reflect loop."),
    ("doc_2", "Tools must be registered in the ToolRegistry before use."),
    ("doc_3", "Long-term memory is persisted to storage/memory/long_term.json."),
]


def main():
    db = VectorDB()
    for doc_id, text in SEED_DOCS:
        db.add(doc_id, text)
        print(f"Seeded: {doc_id}")
    print("Done.")


if __name__ == "__main__":
    main()
