#!/usr/bin/env python3
"""Hamed AI Telegram bot entry point.

Telegram and OpenAI are required. Database, Twilio, Paymob and additional AI
providers are optional. The FastAPI health endpoint runs beside Telegram.
"""
from __future__ import annotations

import os
import threading
import time

from dotenv import load_dotenv
import telebot
import uvicorn

from app.agents.orchestrator import HamedOrchestrator
from app.agents.provider import OpenAIProvider

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5")
HAMED_NAME = os.getenv("HAMED_NAME", "Hamed AI")
PORT = int(os.getenv("PORT", "8000"))


def validate_required_secrets() -> None:
    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")
    if missing:
        raise RuntimeError("Missing required environment variable(s): " + ", ".join(missing))


validate_required_secrets()

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode=None)
hamed = HamedOrchestrator(OpenAIProvider(OPENAI_API_KEY, OPENAI_MODEL))


def status_text() -> str:
    return (
        f"🟢 {HAMED_NAME} ONLINE\n\n"
        "📡 Telegram: CONNECTED\n"
        "🧠 AI Core: READY\n"
        "🤖 80+ specialist agents: READY\n"
        "📚 Learning Council: READY\n"
        "🔎 Client Research Team: READY\n"
        "🛡️ Safety & approvals: ACTIVE\n\n"
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
        "/brains — عرض فريق الوكلاء\n"
        "/learn — بحث تعلمي في علم النفس/المبيعات/الخدمات\n"
        "/reset — بدء محادثة جديدة\n\n"
        "ثم اكتب طلبك مباشرة.",
    )


@bot.message_handler(commands=["brains"])
def handle_brains(message):
    names = hamed.available_agents()
    learning = ", ".join(hamed.learning_agents())
    clients = ", ".join(hamed.client_research_agents())
    bot.send_message(
        message.chat.id,
        f"🤖 الوكلاء المتاحون: {len(names)}+\n\n"
        f"📚 Learning Council: {learning}\n\n"
        f"🎯 Client Research Team: {clients}",
    )


@bot.message_handler(commands=["learn"])
def handle_learn(message):
    topic = (message.text or "").partition(" ")[2].strip()
    if not topic:
        topic = "علم النفس في التواصل مع العملاء واستراتيجيات البيع وخدمة العملاء"
    bot.send_chat_action(message.chat.id, "typing")
    try:
        evidence = hamed.research_for_learning(topic)
        bot.send_message(message.chat.id, "📚 نتيجة البحث التعلمي (للمراجعة):\n\n" + evidence[:3900])
    except Exception as exc:
        print(f"Learning error: {type(exc).__name__}: {exc}", flush=True)
        bot.send_message(message.chat.id, "تعذر تشغيل البحث التعلمي الآن. حاول مرة أخرى.")


@bot.message_handler(commands=["reset"])
def handle_reset(message):
    hamed.reset(str(message.chat.id))
    bot.send_message(message.chat.id, "تم تصفير سياق المحادثة ونبدأ من جديد ✅")


@bot.message_handler(func=lambda m: True, content_types=["text"])
def handle_text(message):
    chat_id = str(message.chat.id)
    user_text = (message.text or "").strip()
    if not user_text:
        return

    bot.send_chat_action(message.chat.id, "typing")
    try:
        reply = hamed.respond(chat_id, user_text)
        if not reply:
            reply = "لم يصلني رد من AI Core. حاول مرة أخرى."
    except Exception as exc:
        print(f"Hamed request error: {type(exc).__name__}: {exc}", flush=True)
        reply = "حصل خطأ مؤقت داخل Hamed. استخدم /status ثم حاول مرة أخرى."

    bot.send_message(message.chat.id, reply)


def start_health_server() -> threading.Thread:
    config = uvicorn.Config("app.main:app", host="0.0.0.0", port=PORT, log_level="info")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, name="hamed-health-server", daemon=True)
    thread.start()
    return thread


def run() -> None:
    print("=" * 52, flush=True)
    print(f"{HAMED_NAME} Telegram Bot is STARTING...", flush=True)
    print("Telegram polling: READY", flush=True)
    print("AI Core: READY", flush=True)
    print("80+ specialist agents: READY", flush=True)
    print("Learning Council: READY", flush=True)
    print("Client Research Team: READY", flush=True)
    print("Health endpoint: http://0.0.0.0:%d/health" % PORT, flush=True)
    print("Database: OPTIONAL", flush=True)
    print("Twilio: OPTIONAL", flush=True)
    print("Paymob: OPTIONAL", flush=True)
    print("=" * 52, flush=True)

    start_health_server()
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)
        except Exception as exc:
            print(f"Telegram polling error: {type(exc).__name__}: {exc}", flush=True)
            time.sleep(5)


if __name__ == "__main__":
    run()
