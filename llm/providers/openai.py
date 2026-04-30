from llm.providers.base_provider import BaseProvider
from openai import OpenAI


class OpenAIProvider(BaseProvider):
    def __init__(self, api_key, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt, **kwargs):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )
        return response.choices[0].message.content

    def complete(self, prompt: str, **kwargs) -> str:
        return self.generate(prompt, **kwargs)

    def chat(self, messages: list[dict], **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs,
        )
        return response.choices[0].message.content
