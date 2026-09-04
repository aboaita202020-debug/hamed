"""
Telegram Channel Adapter — spec section 15 & 21.

"يجب فصل Channel Layer عن Business Logic": this file ONLY translates
Telegram updates into HamedOrchestrator.dispatch(...) calls and
formats the result back into a message. It contains zero business
rules — those all live in app/agents/*.

Requires `python-telegram-bot>=20` (see requirements.txt) and
TELEGRAM_BOT_TOKEN. Both are optional: if the package isn't
installed, importing this module raises a clear, contained error
telling the operator exactly what to install — it does NOT crash the
rest of the app (see scripts/run_telegram.py for the guarded entrypoint).
"""
from __future__ import annotations

from app.config import settings
from app.agents.orchestrator import HamedOrchestrator
from app.logging_config import get_logger

logger = get_logger(__name__)

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes
    _TELEGRAM_AVAILABLE = True
except ImportError:  # pragma: no cover - exercised only when dependency missing
    _TELEGRAM_AVAILABLE = False


def build_telegram_app(orchestrator: HamedOrchestrator):
    """Build (but do not run) the Telegram Application. Raises a clear
    RuntimeError if the dependency or the token is missing, instead of
    a confusing stack trace deep inside python-telegram-bot."""
    if not _TELEGRAM_AVAILABLE:
        raise RuntimeError(
            "python-telegram-bot is not installed. Run: "
            "pip install 'python-telegram-bot>=20,<21'"
        )
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in the environment.")

    app = Application.builder().token(settings.telegram_bot_token).build()

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            "Hamed AI جاهز.\n"
            "/dashboard - ملخص الأداء\n"
            "/leads - آخر العملاء المحتملين\n"
            "/opportunities - أفضل الفرص\n"
        )

    async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        snapshot = orchestrator.dashboard()
        pipeline = snapshot.get("pipeline", {})
        text = (
            f"Leads: {snapshot.get('leads', 0)}\n"
            f"Opportunities: {snapshot.get('opportunities', 0)}\n"
            f"Agent errors: {snapshot.get('agent_errors', 0)}\n"
            f"Open deals: {pipeline.get('total_deals', 0)}\n"
            f"Won: {pipeline.get('won_deals', 0)} "
            f"({pipeline.get('close_rate_pct', 0)}%)\n"
            f"Expected revenue: {pipeline.get('expected_revenue', 0)}\n"
            f"Actual revenue: {pipeline.get('actual_revenue', 0)}\n"
        )
        await update.message.reply_text(text)

    async def leads(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        rows = orchestrator.repo.list_leads()[:10]
        if not rows:
            await update.message.reply_text("لا يوجد Leads بعد.")
            return
        text = "\n".join(f"- {l.name} ({l.stage}) score={l.score}" for l in rows)
        await update.message.reply_text(text)

    async def opportunities(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        rows = orchestrator.repo.list_opportunities()[:10]
        if not rows:
            await update.message.reply_text("لا يوجد فرص مسجلة بعد.")
            return
        text = "\n".join(
            f"- {o.opp_type} score={o.opportunity_score} value={o.potential_value}"
            for o in rows
        )
        await update.message.reply_text(text)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dashboard", dashboard))
    app.add_handler(CommandHandler("leads", leads))
    app.add_handler(CommandHandler("opportunities", opportunities))

    return app
