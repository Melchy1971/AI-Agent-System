from llm.providers.base_provider import BaseProvider


class LocalModelProvider(BaseProvider):
    """Ollama-compatible local model provider."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3"):
        self._base_url = base_url
        self._model = model

    def generate(self, prompt: str, **kwargs) -> str:
        return self.chat([{"role": "user", "content": prompt}], **kwargs)

    def complete(self, prompt: str, **kwargs) -> str:
        return self.generate(prompt, **kwargs)

    def chat(self, messages: list[dict], **kwargs) -> str:
        import httpx
        payload = {"model": self._model, "messages": messages, "stream": False}
        r = httpx.post(f"{self._base_url}/api/chat", json=payload, timeout=120)
        r.raise_for_status()
        return r.json()["message"]["content"]
