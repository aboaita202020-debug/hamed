#!/usr/bin/env python3
"""Hamed AI runtime: Telegram interface + independent 24/7 autonomous core."""
from __future__ import annotations

import os
import threading
import time

from dotenv import load_dotenv
import telebot
import uvicorn

from app.agents.orchestrator import HamedOrchestrator
from app.agents.provider import MultiBrainProvider
from app.agents.autonomous_core import AutonomousCore
from app.voice.telegram_tts import TelegramTTS

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
HAMED_NAME = os.getenv("HAMED_NAME", "Hamed AI")
PORT = int(os.getenv("PORT", "8000"))
TELEGRAM_POLLING_ENABLED = os.getenv("HAMED_TELEGRAM_POLLING", "true").lower() == "true"
AUTONOMOUS_NOTIFY_CHAT_ID = os.getenv("HAMED_AUTONOMOUS_NOTIFY_CHAT_ID", "").strip()


def validate_required_secrets() -> None:
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("Missing required environment variable(s): TELEGRAM_BOT_TOKEN")
    if not OPENAI_API_KEY:
        raise RuntimeError("Missing required environment variable(s): OPENAI_API_KEY")


validate_required_secrets()
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode=None)
hamed = HamedOrchestrator(MultiBrainProvider())
voice_tts = TelegramTTS()


def autonomous_notify(text: str) -> None:
    if not AUTONOMOUS_NOTIFY_CHAT_ID:
        print(text, flush=True)
        return
    try:
        bot.send_message(int(AUTONOMOUS_NOTIFY_CHAT_ID), text)
    except Exception as exc:
        print(f"Autonomous notification error: {type(exc).__name__}: {exc}", flush=True)


# This core runs independently of Telegram polling. Telegram is only an interface/notification channel.
autonomous_core = AutonomousCore(hamed, notify=autonomous_notify)


def send_hamed_reply(chat_id: int, reply: str) -> None:
    """Prefer free voice output; always fall back to text if TTS/network fails."""
    if voice_tts.enabled:
        audio_path = voice_tts.synthesize(reply)
        if audio_path:
            try:
                with open(audio_path, "rb") as audio:
                    bot.send_audio(chat_id, audio, title="Hamed AI")
                return
            except Exception as exc:
                print(f"Voice send error: {type(exc).__name__}: {exc}", flush=True)
            finally:
                voice_tts.cleanup(audio_path)
    bot.send_message(chat_id, reply)


def status_text() -> str:
    """Build status without calling any AI provider or network service."""
    try:
        brains = ", ".join(hamed.provider.available_brains()) or "none"
    except Exception as exc:
        brains = "unavailable (" + type(exc).__name__ + ")"
    try:
        voice_status = "READY" if voice_tts.enabled else "OFF"
    except Exception as exc:
        voice_status = "ERROR (" + type(exc).__name__ + ")"
    return (
        f"🟢 {HAMED_NAME} ONLINE\n\n"
        "🧠 Autonomous Core: 24/7 READY\n"
        f"🧠 AI Brains: {brains}\n"
        "🤖 80+ specialist agents: READY\n"
        "📚 Learning Council: READY\n"
        "🎯 Client Research Team: READY\n"
        "🛡️ Safety & approvals: ACTIVE\n"
        f"🔊 Voice Reply: {voice_status}\n"
        "📡 Telegram: INTERFACE ONLY\n\n"
        "اكتب /help لمعرفة الأوامر."
    )


@bot.message_handler(commands=["start", "status"])
def handle_start(message):
    """Status is local-only and must never fail because an AI provider is unavailable."""
    try:
        bot.send_message(message.chat.id, status_text())
    except Exception as exc:
        print(f"Status send error: {type(exc).__name__}: {exc}", flush=True)


@bot.message_handler(func=lambda m: (m.text or "").strip().lower() in {"status", "ستاتس", "ستيتس"}, content_types=["text"])
def handle_status_text(message):
    """Also accept a plain status message without requiring the slash command."""
    try:
        bot.send_message(message.chat.id, status_text())
    except Exception as exc:
        print(f"Status text send error: {type(exc).__name__}: {exc}", flush=True)


@bot.message_handler(commands=["help"])
def handle_help(message):
    bot.send_message(message.chat.id, "أوامر حامد:\n\n/start — تشغيل واختبار الاتصال\n/status — حالة النظام\n/brains — عرض فريق الوكلاء والعقول\n/learn — بحث تعلمي\n/reset — بدء محادثة جديدة\n\n🔊 الرد الصوتي يعمل تلقائياً عند نجاح خدمة الصوت.\n\nثم اكتب طلبك مباشرة.")


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
    send_hamed_reply(message.chat.id, reply)


def start_health_server() -> threading.Thread:
    config = uvicorn.Config("app.main:app", host="0.0.0.0", port=PORT, log_level="warning")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, name="hamed-health-server", daemon=True)
    thread.start()
    return thread


def run() -> None:
    print(f"{HAMED_NAME} runtime STARTING...", flush=True)
    print("Autonomous Core / Multi-Brain / agents / learning / approvals: READY", flush=True)
    print("Telegram is an interface; autonomous core is independent of Telegram polling.", flush=True)
    print("Database / Twilio / Paymob: OPTIONAL", flush=True)
    start_health_server()
    autonomous_core.start()
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
