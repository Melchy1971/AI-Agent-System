from pathlib import Path


TEMPLATES_DIR = Path(__file__).parent / "templates"


class PromptLoader:
    _cache: dict[str, str] = {}

    @classmethod
    def load(cls, name: str, **kwargs) -> str:
        """Load a prompt template by filename (without .txt) and interpolate kwargs."""
        if name not in cls._cache:
            path = TEMPLATES_DIR / f"{name}.txt"
            if not path.exists():
                raise FileNotFoundError(f"Prompt template not found: {path}")
            cls._cache[name] = path.read_text(encoding="utf-8")
        return cls._cache[name].format(**kwargs)
