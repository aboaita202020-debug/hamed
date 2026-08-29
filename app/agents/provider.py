"""AI provider abstraction; external providers can be added without changing agents."""
from typing import Protocol


class AIProvider(Protocol):
    def generate_response(self, messages: list[dict[str, str]], *, system: str = "") -> str:
        ...


class OpenAIProvider:
    def __init__(self, api_key: str, model: str = "gpt-5") -> None:
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required to use OpenAIProvider")
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install the openai package to use OpenAIProvider") from exc
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_response(self, messages: list[dict[str, str]], *, system: str = "") -> str:
        payload = list(messages)
        if system:
            payload.insert(0, {"role": "system", "content": system})
        response = self.client.responses.create(model=self.model, input=payload)
        return response.output_text.strip()
