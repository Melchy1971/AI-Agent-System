from llm.providers.base_provider import BaseProvider


class AnthropicProvider(BaseProvider):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6"):
        import anthropic
        self._client = anthropic.Anthropic(api_key=api_key)
        self._model = model

    def generate(self, prompt: str, **kwargs) -> str:
        return self.chat([{"role": "user", "content": prompt}], **kwargs)

    def complete(self, prompt: str, **kwargs) -> str:
        return self.generate(prompt, **kwargs)

    def chat(self, messages: list[dict], max_tokens: int = 4096, **kwargs) -> str:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=max_tokens,
            messages=messages,
            **kwargs,
        )
        return response.content[0].text
