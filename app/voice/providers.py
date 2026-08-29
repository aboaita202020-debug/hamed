"""Provider configuration for Hamed's cloud voice stack.

Hamed uses Twilio for PSTN/phone connectivity and OpenAI Realtime for the
conversation engine. Secrets are read only from environment variables.
"""
from dataclasses import dataclass
import os


@dataclass(frozen=True)
class VoiceProviders:
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_from_number: str
    openai_api_key: str
    openai_realtime_url: str

    @classmethod
    def from_env(cls) -> "VoiceProviders":
        values = {
            "twilio_account_sid": os.getenv("TWILIO_ACCOUNT_SID", ""),
            "twilio_auth_token": os.getenv("TWILIO_AUTH_TOKEN", ""),
            "twilio_from_number": os.getenv("TWILIO_FROM_NUMBER", ""),
            "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
            "openai_realtime_url": os.getenv(
                "OPENAI_REALTIME_URL",
                "wss://api.openai.com/v1/realtime?model=gpt-realtime-2.1-mini",
            ),
        }
        missing = [key for key, value in values.items() if not value]
        if missing:
            raise RuntimeError("Missing voice provider configuration: " + ", ".join(missing))
        return cls(**values)

    def public_status(self) -> dict[str, str | bool]:
        return {
            "twilio_configured": bool(self.twilio_account_sid and self.twilio_from_number),
            "openai_configured": bool(self.openai_api_key),
            "realtime_configured": bool(self.openai_realtime_url),
        }
