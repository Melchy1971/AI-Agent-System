import json
from pathlib import Path
from typing import Any


class LongTermStore:
    """Key-value store backed by a JSON file."""

    def __init__(self, path: str = "storage/memory/long_term.json"):
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._data: dict[str, Any] = self._load()

    def _load(self) -> dict[str, Any]:
        if self._path.exists():
            return json.loads(self._path.read_text(encoding="utf-8"))
        return {}

    def _save(self) -> None:
        self._path.write_text(json.dumps(self._data, indent=2), encoding="utf-8")

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
        self._save()

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def delete(self, key: str) -> None:
        self._data.pop(key, None)
        self._save()

    def keys(self) -> list[str]:
        return list(self._data.keys())
