#!/usr/bin/env python3
"""Hamed AI Telegram entry point.

Runs the Telegram channel and routes requests through the common Hamed
orchestrator. Secrets are read only from environment variables.
"""
import os
import time
from dotenv import load_dotenv
import telebot
from app.agents.orchestrator import HamedOrchestrator
from app.agents.provider import OpenAIProvider

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5")
HAMED_NAME = os.getenv("HAMED_NAME", "Hamed AI")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is missing. Add it as a deployment secret.")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode=None)
hamed = None
if OPENAI_API_KEY:
    hamed = HamedOrchestrator(OpenAIProvider(OPENAI_API_KEY, OPENAI_MODEL))


def status_text() -> str:
    ai = "READY" if hamed else "WAITING_FOR_AI_KEY"
    return (
        f"🟢 {HAMED_NAME} ONLINE\n\n"
        "📡 Telegram: CONNECTED\n"
        f"🧠 AI Core: {ai}\n"
        "🛡️ Safety: ACTIVE\n"
        "🤖 Orchestrator: READY\n\n"
        "اكتب /help لمعرفة الأوامر."
    )


@bot.message_handler(commands=["start", "status"])
def handle_start(message):
    bot.send_message(message.chat.id, status_text())


@bot.message_handler(commands=["help"])
def handle_help(message):
    bot.send_message(
        message.chat.id,
        "أوامر حامد:\n\n"
        "/start — تشغيل واختبار الاتصال\n"
        "/status — حالة النظام\n"
        "/reset — بدء محادثة جديدة\n\n"
        "ثم اكتب طلبك مباشرة.",
    )


@bot.message_handler(commands=["reset"])
def handle_reset(message):
    if hamed:
        hamed.reset(str(message.chat.id))
    bot.send_message(message.chat.id, "تم تصفير سياق المحادثة ونبدأ من جديد ✅")


@bot.message_handler(func=lambda m: True, content_types=["text"])
def handle_text(message):
    chat_id = str(message.chat.id)
    user_text = (message.text or "").strip()
    if not user_text:
        return

    bot.send_chat_action(message.chat.id, "typing")

    if not hamed:
        bot.send_message(
            message.chat.id,
            "🟡 Telegram متصل وحامد شغال، لكن AI Core محتاج OPENAI_API_KEY في Secrets.\n"
            "لن أقول إن الذكاء الاصطناعي شغال قبل ما يكون متصل فعليًا.",
        )
        return

    try:
        reply = hamed.respond(chat_id, user_text)
        if not reply:
            reply = "لم يصلني رد من AI Core. حاول مرة أخرى."
    except Exception as exc:
        print(f"Hamed request error: {type(exc).__name__}: {exc}", flush=True)
        reply = "حصل خطأ مؤقت داخل Hamed. استخدم /status ثم حاول مرة أخرى."

    bot.send_message(message.chat.id, reply)


if __name__ == "__main__":
    print("=" * 52, flush=True)
    print(f"{HAMED_NAME} Telegram Bot is STARTING...", flush=True)
    print("Telegram polling: READY", flush=True)
    print(f"AI Core: {'READY' if hamed else 'WAITING_FOR_OPENAI_API_KEY'}", flush=True)
    print("=" * 52, flush=True)
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)
        except Exception as exc:
            print(f"Telegram polling error: {type(exc).__name__}: {exc}", flush=True)
            time.sleep(5)
