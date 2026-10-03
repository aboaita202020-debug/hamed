"""Free-first Telegram voice reply helper for Hamed AI."""
from __future__ import annotations

import os
import tempfile
from typing import Optional


class TelegramTTS:
    """Generate Arabic speech as MP3 without changing Hamed's AI core."""

    def __init__(self) -> None:
        self.enabled = os.getenv("HAMED_VOICE_REPLY", "true").lower() == "true"
        self.language = os.getenv("HAMED_VOICE_LANGUAGE", "ar")
        self.tld = os.getenv("HAMED_VOICE_TLD", "com.eg")
        self.max_chars = int(os.getenv("HAMED_VOICE_MAX_CHARS", "3500"))

    def synthesize(self, text: str) -> Optional[str]:
        if not self.enabled or not text.strip():
            return None
        try:
            from gtts import gTTS
        except Exception:
            return None

        text = text.strip()[: self.max_chars]
        fd, path = tempfile.mkstemp(prefix="hamed_voice_", suffix=".mp3")
        os.close(fd)
        try:
            gTTS(text=text, lang=self.language, tld=self.tld, slow=False).save(path)
            return path
        except Exception:
            try:
                os.remove(path)
            except OSError:
                pass
            return None

    @staticmethod
    def cleanup(path: Optional[str]) -> None:
        if not path:
            return
        try:
            os.remove(path)
        except OSError:
            pass
