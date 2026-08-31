"""Telegram adapter for Hamed AI.

Secrets are read from environment variables; no bot token is stored in source.
"""
from __future__ import annotations

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from ..agents.orchestrator import HamedOrchestrator
from ..config import settings

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message:
        await update.effective_message.reply_text(
            "أهلًا، أنا حامد 🤖\nاكتب لي هدفك أو طلبك وسأحلله وأساعدك في تحويله إلى خطوات عملية."
        )


async def chat_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_message or not update.effective_user:
        return
    text = update.effective_message.text or ""
    if not text.strip():
        return

    orchestrator: HamedOrchestrator = context.application.bot_data["orchestrator"]
    session_id = f"telegram:{update.effective_user.id}"
    try:
        reply = orchestrator.respond(session_id, text)
    except Exception:
        logger.exception("Telegram request failed")
        reply = "حصل خطأ مؤقت أثناء معالجة طلبك. حاول مرة أخرى."
    await update.effective_message.reply_text(reply)


def build_telegram_application(orchestrator: HamedOrchestrator) -> Application:
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured")

    application = Application.builder().token(settings.telegram_bot_token).build()
    application.bot_data["orchestrator"] = orchestrator
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_message))
    return application


def run_telegram_bot(orchestrator: HamedOrchestrator) -> None:
    application = build_telegram_application(orchestrator)
    application.run_polling(allowed_updates=Update.ALL_TYPES)
