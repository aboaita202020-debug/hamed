"""
Central configuration for Hamed AI.

Every setting is read from environment variables (see .env.example).
Nothing here requires a third-party package. Secrets are NEVER
hard-coded and NEVER logged (see AuditLog.redact()).

Design rule from the spec (section 23/33):
    Database, Telegram, OpenAI, Twilio, Paymob are all OPTIONAL for
    Core to boot. A missing var simply disables the related feature
    instead of crashing the process.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field


def _env_bool(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


def _env_float(name: str, default: float) -> float:
    val = os.getenv(name)
    try:
        return float(val) if val is not None else default
    except ValueError:
        return default


@dataclass
class ApprovalLimits:
    """Thresholds above which an action requires human Approval.
    Owner-configurable via env vars (spec section 13)."""

    max_auto_payment_egp: float = field(
        default_factory=lambda: _env_float("HAMED_MAX_AUTO_PAYMENT_EGP", 0.0)
    )
    max_auto_purchase_egp: float = field(
        default_factory=lambda: _env_float("HAMED_MAX_AUTO_PURCHASE_EGP", 0.0)
    )
    max_auto_discount_pct: float = field(
        default_factory=lambda: _env_float("HAMED_MAX_AUTO_DISCOUNT_PCT", 10.0)
    )
    max_negotiation_concession_pct: float = field(
        default_factory=lambda: _env_float("HAMED_MAX_NEGOTIATION_CONCESSION_PCT", 15.0)
    )
    require_approval_for_contracts: bool = field(
        default_factory=lambda: _env_bool("HAMED_REQUIRE_APPROVAL_CONTRACTS", True)
    )


@dataclass
class Settings:
    # --- Core ---
    app_name: str = "Hamed AI"
    environment: str = field(default_factory=lambda: os.getenv("HAMED_ENV", "development"))
    debug: bool = field(default_factory=lambda: _env_bool("HAMED_DEBUG", False))

    # --- Database (optional; falls back to local SQLite file, stdlib only) ---
    database_url: str = field(
        default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///./data/hamed.db")
    )

    # --- Telegram (optional) ---
    telegram_bot_token: str | None = field(
        default_factory=lambda: os.getenv("TELEGRAM_BOT_TOKEN")
    )

    # --- AI Providers (optional, at least one recommended) ---
    openai_api_key: str | None = field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    anthropic_api_key: str | None = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"))
    deepseek_api_key: str | None = field(default_factory=lambda: os.getenv("DEEPSEEK_API_KEY"))
    mistral_api_key: str | None = field(default_factory=lambda: os.getenv("MISTRAL_API_KEY"))
    default_ai_provider: str = field(
        default_factory=lambda: os.getenv("HAMED_DEFAULT_AI_PROVIDER", "openai")
    )

    # --- Payments / Voice (optional) ---
    twilio_account_sid: str | None = field(default_factory=lambda: os.getenv("TWILIO_ACCOUNT_SID"))
    twilio_auth_token: str | None = field(default_factory=lambda: os.getenv("TWILIO_AUTH_TOKEN"))
    paymob_api_key: str | None = field(default_factory=lambda: os.getenv("PAYMOB_API_KEY"))

    # --- Web server (optional dashboard adapter) ---
    host: str = field(default_factory=lambda: os.getenv("HAMED_HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(os.getenv("PORT", os.getenv("HAMED_PORT", "8000"))))

    approval_limits: ApprovalLimits = field(default_factory=ApprovalLimits)

    def sqlite_path(self) -> str:
        """Extract a plain filesystem path out of a sqlite:/// URL."""
        if self.database_url.startswith("sqlite:///"):
            return self.database_url[len("sqlite:///"):]
        # Fallback: treat the whole string as a path
        return self.database_url

    def configured_ai_providers(self) -> list[str]:
        providers = []
        if self.openai_api_key:
            providers.append("openai")
        if self.anthropic_api_key:
            providers.append("claude")
        if self.deepseek_api_key:
            providers.append("deepseek")
        if self.mistral_api_key:
            providers.append("mistral")
        return providers


settings = Settings()
