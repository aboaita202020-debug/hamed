#!/usr/bin/env python3
"""
bot.py
نقطة دخول بسيطة لنسخة MVP: polling-based Telegram bot.
يعتمد على telebot (pyTelegramBotAPI) و agent.py للاتصال بـ Claude.
"""
import os
from dotenv import load_dotenv
import telebot
from agent import Agent

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not TELEGRAM_BOT_TOKEN or not ANTHROPIC_API_KEY:
    raise RuntimeError("Please set TELEGRAM_BOT_TOKEN and ANTHROPIC_API_KEY in your environment (.env)")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
# حافظ على وكلاء منفصلين لكل محادثة (chat_id)
agents = {}

def get_agent_for_chat(chat_id: int) -> Agent:
    if chat_id not in agents:
        agents[chat_id] = Agent(api_key=ANTHROPIC_API_KEY)
    return agents[chat_id]

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    text = (
        "أهلاً! أنا بوت ذكي مبني على Claude (MVP).\n\n"
        "استخدم /reset لمسح سياق المحادثة.\n"
        "ابعتلي أي رسالة وسأرد عليك."
    )
    bot.send_message(chat_id, text)

@bot.message_handler(commands=['reset'])
def handle_reset(message):
    chat_id = message.chat.id
    agent = get_agent_for_chat(chat_id)
    agent.reset()
    bot.send_message(chat_id, "سياق المحادثة اتعمله Reset. نبدأ من جديد ✅")

@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    user_text = message.text.strip()
    agent = get_agent_for_chat(chat_id)
    # أضف رسالة المستخدم إلى السياق واستدعي الوكيل
    bot.send_chat_action(chat_id, 'typing')
    try:
        reply = agent.get_response(user_text)
    except Exception as e:
        reply = f"حصل خطأ أثناء التعامل مع API: {e}"
    bot.send_message(chat_id, reply)

if __name__ == "__main__":
    print("Starting Telegram bot (polling). Press Ctrl+C to stop.")
    bot.infinity_polling()
