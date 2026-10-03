from dataclasses import dataclass
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class ApprovalLimits:
    max_auto_payment_egp: float = 0.0
    max_auto_purchase_egp: float = 0.0
    max_auto_discount_pct: float = 10.0
    max_negotiation_concession_pct: float = 15.0
    require_approval_for_contracts: bool = True


class Settings(BaseSettings):
    app_name: str = "ORVIA AGI"
    environment: str = "development"
    host: str = "0.0.0.0"
    port: int = 8000
    auto_execution_enabled: bool = True
    autonomous_enabled: bool = True
    autonomous_max_targets: int = 10
    require_approval_for_financial_actions: bool = True
    min_opportunity_score: float = 0.60
    openai_api_key: str | None = None
    openai_model: str = "gpt-5-mini"
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini"
    deepseek_api_key: str | None = None
    deepseek_model: str = "deepseek-chat"
    kimi_api_key: str | None = None
    kimi_model: str = "kimi"
    youtube_enabled: bool = False
    youtube_client_id: str | None = None
    youtube_client_secret: str | None = None
    youtube_kids_channel_id: str | None = None
    youtube_islamic_channel_id: str | None = None
    telegram_bot_token: str | None = None
    whatsapp_access_token: str | None = None
    whatsapp_phone_number_id: str | None = None
    approval_limits: ApprovalLimits = ApprovalLimits()
    model_config = SettingsConfigDict(env_file=PROJECT_ROOT / ".env", extra="ignore")


settings = Settings()