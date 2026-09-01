#!/usr/bin/env python3
"""Hamed AI Telegram runtime with an HTTP health server."""
from __future__ import annotations

import os
import threading
import time

from dotenv import load_dotenv
import telebot
import uvicorn

from app.agents.orchestrator import HamedOrchestrator
from app.agents.provider import MultiBrainProvider

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
HAMED_NAME = os.getenv("HAMED_NAME", "Hamed AI")
PORT = int(os.getenv("PORT", "8000"))
TELEGRAM_POLLING_ENABLED = os.getenv("HAMED_TELEGRAM_POLLING", "true").lower() == "true"


def validate_required_secrets() -> None:
    missing = [
        name for name, value in (
            ("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN),
            ("OPENAI_API_KEY", OPENAI_API_KEY),
        ) if not value
    ]
    if missing:
        raise RuntimeError("Missing required environment variable(s): " + ", ".join(missing))


validate_required_secrets()
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode=None)
hamed = HamedOrchestrator(MultiBrainProvider())


def status_text() -> str:
    brains = ", ".join(hamed.provider.available_brains())
    return (
        f"🟢 {HAMED_NAME} ONLINE\n\n"
        "📡 Telegram: CONNECTED\n"
        f"🧠 AI Brains: {brains}\n"
        "🤖 80+ specialist agents: READY\n"
        "📚 Learning Council: READY\n"
        "🎯 Client Research Team: READY\n"
        "🛡️ Safety & approvals: ACTIVE\n\n"
        "اكتب /help لمعرفة الأوامر."
    )


@bot.message_handler(commands=["start", "status"])
def handle_start(message):
    bot.send_message(message.chat.id, status_text())


@bot.message_handler(commands=["help"])
def handle_help(message):
    bot.send_message(message.chat.id, "أوامر حامد:\n\n/start — تشغيل واختبار الاتصال\n/status — حالة النظام\n/brains — عرض فريق الوكلاء والعقول\n/learn — بحث تعلمي\n/reset — بدء محادثة جديدة\n\nثم اكتب طلبك مباشرة.")


@bot.message_handler(commands=["brains"])
def handle_brains(message):
    names = hamed.available_agents()
    learning = ", ".join(hamed.learning_agents())
    clients = ", ".join(hamed.client_research_agents())
    brains = ", ".join(hamed.provider.available_brains())
    bot.send_message(message.chat.id, f"🤖 الوكلاء: {len(names)}+\n🧠 العقول المتصلة: {brains}\n\n📚 Learning Council: {learning}\n\n🎯 Client Research Team: {clients}")


@bot.message_handler(commands=["learn"])
def handle_learn(message):
    topic = (message.text or "").partition(" ")[2].strip() or "علم النفس في التواصل مع العملاء واستراتيجيات البيع وخدمة العملاء"
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
    chat_id, user_text = str(message.chat.id), (message.text or "").strip()
    if not user_text:
        return
    bot.send_chat_action(message.chat.id, "typing")
    try:
        reply = hamed.respond(chat_id, user_text) or "لم يصلني رد من AI Core. حاول مرة أخرى."
    except Exception as exc:
        print(f"Hamed request error: {type(exc).__name__}: {exc}", flush=True)
        reply = "حصل خطأ مؤقت داخل Hamed. استخدم /status ثم حاول مرة أخرى."
    bot.send_message(message.chat.id, reply)


def start_health_server() -> threading.Thread:
    config = uvicorn.Config("app.main:app", host="0.0.0.0", port=PORT, log_level="warning")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, name="hamed-health-server", daemon=True)
    thread.start()
    return thread


def run() -> None:
    print(f"{HAMED_NAME} Telegram runtime STARTING...", flush=True)
    print("Multi-Brain / agents / learning / approvals: READY", flush=True)
    print("Database / Twilio / Paymob: OPTIONAL", flush=True)
    start_health_server()
    if not TELEGRAM_POLLING_ENABLED:
        print("Telegram polling: DISABLED (test mode)", flush=True)
        while True:
            time.sleep(60)
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)
        except Exception as exc:
            print(f"Telegram polling error: {type(exc).__name__}: {exc}", flush=True)
            time.sleep(5)


if __name__ == "__main__":
    run()
