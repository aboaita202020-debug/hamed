from __future__ import annotations

import time
from dataclasses import dataclass

from .config import settings


@dataclass
class ModelResult:
    text: str
    model: str
    connected: bool = True


class OpenAIProvider:
    """Minimal, secret-safe OpenAI Responses API adapter."""

    def __init__(self) -> None:
        self._client = None
        self._last_check_at = 0.0
        self._last_check_ok = False
        self._last_error = ""

    @property
    def configured(self) -> bool:
        return bool(settings.openai_api_key)

    @property
    def model(self) -> str:
        return settings.openai_model

    def _get_client(self):
        if not self.configured:
            return None
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(api_key=settings.openai_api_key)
        return self._client

    def check_connection(self, force: bool = False) -> dict:
        if not self.configured:
            return {"configured": False, "connected": False, "model": self.model}
        now = time.monotonic()
        if not force and now - self._last_check_at < 300:
            return {
                "configured": True,
                "connected": self._last_check_ok,
                "model": self.model,
                **({"error": self._last_error} if self._last_error else {}),
            }
        try:
            response = self._get_client().responses.create(
                model=self.model,
                input="Reply with exactly: ORVIA_OK",
                max_output_tokens=8,
            )
            ok = response.output_text.strip() == "ORVIA_OK"
            self._last_check_ok = ok
            self._last_error = "" if ok else "unexpected model response"
        except Exception as exc:  # noqa: BLE001 - provider SDK boundary
            self._last_check_ok = False
            self._last_error = f"{type(exc).__name__}: {exc}"
        self._last_check_at = now
        result = {"configured": True, "connected": self._last_check_ok, "model": self.model}
        if self._last_error:
            result["error"] = self._last_error
        return result

    def generate(self, prompt: str) -> ModelResult:
        client = self._get_client()
        if client is None:
            return ModelResult(
                text="OpenAI غير مضبوط؛ تم تشغيل المهمة في وضع المحاكاة الآمن.",
                model="offline",
                connected=False,
            )
        response = client.responses.create(
            model=self.model,
            input=prompt,
            max_output_tokens=900,
        )
        return ModelResult(
            text=response.output_text,
            model=self.model,
            connected=True,
        )


openai_provider = OpenAIProvider()
