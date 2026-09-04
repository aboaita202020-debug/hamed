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
    telegram_chat_id: str | None = os.getenv("TELEGRAM_CHAT_ID")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///hamed.db")
    app_env: str = os.getenv("APP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    # Autonomous mode is the default operating mode. Execution remains bounded
    # by the server-side policy and platform/legal constraints.
    autonomous_mode: bool = os.getenv("HAMED_AUTONOMOUS_MODE", "true").lower() == "true"
    max_purchase_value: float = float(os.getenv("HAMED_MAX_PURCHASE_VALUE", "0"))
    max_payment_value: float = float(os.getenv("HAMED_MAX_PAYMENT_VALUE", "0"))
    max_discount_percent: float = float(os.getenv("HAMED_MAX_DISCOUNT_PERCENT", "20"))
    whatsapp_number: str | None = os.getenv("HAMED_WHATSAPP_NUMBER")
    vodafone_cash_wallets: tuple[str, ...] = tuple(x.strip() for x in os.getenv("HAMED_VODAFONE_CASH_WALLETS", "").split(",") if x.strip())
    opportunity_hunter_enabled: bool = os.getenv("HAMED_OPPORTUNITY_HUNTER", "true").lower() == "true"
    opportunity_interval: int = max(300, int(os.getenv("HAMED_OPPORTUNITY_INTERVAL", "1800")))


settings = Settings()
