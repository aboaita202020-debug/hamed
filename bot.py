#!/usr/bin/env python3
"""Telegram entry point for Hamed AI."""
import os
from dotenv import load_dotenv
import telebot
from app.agents.orchestrator import HamedOrchestrator
from app.agents.provider import OpenAIProvider

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("Please set TELEGRAM_BOT_TOKEN in your environment (.env)")
if not OPENAI_API_KEY:
    raise RuntimeError("Please set OPENAI_API_KEY in your environment (.env)")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
hamed = HamedOrchestrator(OpenAIProvider(OPENAI_API_KEY, OPENAI_MODEL))

@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "أهلاً! أنا حامد AI 🤖\n\nأقدر أساعدك في المبيعات، المشتريات، تحليل الفرص التجارية، وحساب الربحية.\n\nاستخدم /reset لبدء محادثة جديدة.")

@bot.message_handler(commands=["reset"])
def handle_reset(message):
    hamed.reset(str(message.chat.id))
    bot.send_message(message.chat.id, "تم تصفير سياق المحادثة ونبدأ من جديد ✅")

@bot.message_handler(func=lambda m: True, content_types=["text"])
def handle_text(message):
    chat_id = str(message.chat.id)
    user_text = (message.text or "").strip()
    bot.send_chat_action(message.chat.id, "typing")
    try:
        reply = hamed.respond(chat_id, user_text)
    except Exception:
        reply = "حصلت مشكلة مؤقتة وأنا بعالج الطلب. حاول مرة تانية بعد قليل."
    bot.send_message(message.chat.id, reply)

if __name__ == "__main__":
    print("Starting Hamed AI Telegram bot (polling). Press Ctrl+C to stop.")
    bot.infinity_polling()
