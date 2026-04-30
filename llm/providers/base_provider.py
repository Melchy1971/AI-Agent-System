from abc import ABC, abstractmethod


class BaseProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Send a prompt and return generated text."""

    @abstractmethod
    def complete(self, prompt: str, **kwargs) -> str:
        """Send a prompt and return the completion text."""

    @abstractmethod
    def chat(self, messages: list[dict], **kwargs) -> str:
        """Send a list of chat messages and return the assistant reply."""
