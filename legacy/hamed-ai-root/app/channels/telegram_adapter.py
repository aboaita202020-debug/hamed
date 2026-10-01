"""
Telegram Channel Adapter — spec section 15 & 21.

"يجب فصل Channel Layer عن Business Logic": this file ONLY translates
Telegram updates into HamedOrchestrator.dispatch(...) calls and
formats the result back into a message. It contains zero business
rules — those all live in app/agents/*.

Requires `python-telegram-bot>=20` (see requirements.txt) and
TELEGRAM_BOT_TOKEN. Both are optional: if the package isn't
installed, importing this module raises a clear, contained error.
"""
from __future__ import annotations

from app.config import settings
from app.agents.orchestrator import HamedOrchestrator
from app.logging_config import get_logger

logger = get_logger(__name__)

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
    _TELEGRAM_AVAILABLE = True
except ImportError:  # pragma: no cover
    _TELEGRAM_AVAILABLE = False


def build_telegram_app(orchestrator: HamedOrchestrator):
    """Build the Telegram Application and connect normal messages to Hamed."""
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
            "\nأرسل لي أي رسالة عادية وسأتعامل معها."
        )

    async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        snapshot = orchestrator.dashboard()
        pipeline = snapshot.get("pipeline", {})
        text = (
            f"Leads: {snapshot.get('leads', 0)}\n"
            f"Opportunities: {snapshot.get('opportunities', 0)}\n"
            f"Agent errors: {snapshot.get('agent_errors', 0)}\n"
            f"Open deals: {pipeline.get('total_deals', 0)}\n"
            f"Won: {pipeline.get('won_deals', 0)} ({pipeline.get('close_rate_pct', 0)}%)\n"
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

    async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not update.message or not update.message.text:
            return
        text = update.message.text.strip()
        if not text:
            return
        await update.message.chat.send_action("typing")
        try:
            result = orchestrator.consult_brains(text)
            if result.get("success"):
                response = result.get("final_answer") or result.get("answer") or result.get("decision")
                if not response:
                    response = str(result)
            else:
                # Keep the bot useful even when the optional AI council is unavailable.
                outcome = orchestrator.dispatch("customer_conversation_agent", {"message": text})
                response = outcome.result.data or outcome.result.error or "لم أتمكن من معالجة الرسالة الآن."
            if isinstance(response, dict):
                response = response.get("message") or response.get("text") or str(response)
            await update.message.reply_text(str(response)[:4000])
        except Exception as exc:
            logger.exception("Telegram message handling failed")
            await update.message.reply_text(f"حدث خطأ أثناء معالجة الرسالة: {exc}")

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dashboard", dashboard))
    app.add_handler(CommandHandler("leads", leads))
    app.add_handler(CommandHandler("opportunities", opportunities))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    return app
