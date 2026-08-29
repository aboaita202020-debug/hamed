"""Environment-backed configuration for Hamed AI."""
from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-5")
    telegram_bot_token: str | None = os.getenv("TELEGRAM_BOT_TOKEN")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///hamed.db")
    app_env: str = os.getenv("APP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
