#!/usr/bin/env python3
"""Reset all storage directories (conversations, memory, files, vector index)."""
import shutil
from pathlib import Path

DIRS = [
    "storage/conversations",
    "storage/memory",
    "storage/files",
    "storage/vector_index",
]


def main():
    for d in DIRS:
        p = Path(d)
        if p.exists():
            shutil.rmtree(p)
        p.mkdir(parents=True)
        (p / ".gitkeep").touch()
        print(f"Reset: {d}")


if __name__ == "__main__":
    main()
