#!/usr/bin/env python3
"""
🤖 Hamed AI Telegram Bot - Complete with AI Integration
Runs 24/7 automatically with 4 AI APIs:
- Anthropic Claude (Primary)
- OpenAI GPT-4 (Fallback 1)
- Kimi Moonshot (Fallback 2)
- Google Gemini (Fallback 3)
"""
import os
import sys
import json
import sqlite3
from datetime import datetime
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed. Using default values.")

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8843221025:AAGtegewAMOalwv1ZAlBlCKwjPI953vfJuU')
ANTHROPIC_KEY = os.getenv('ANTHROPIC_API_KEY', '')
OPENAI_KEY = os.getenv('OPENAI_API_KEY', '')
KIMI_KEY = os.getenv('KIMI_API_KEY', '')
GEMINI_KEY = os.getenv('GEMINI_API_KEY', '')
WHATSAPP = os.getenv('WHATSAPP_NUMBER', '01061245527')
VODAFONE_CASH = os.getenv('VODAFONE_CASH', '01061245527')

# Database setup
DB_PATH = Path('telegram_bot.db')

def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            joined_at TEXT,
            last_active TEXT,
            message_count INTEGER DEFAULT 0
        )
    """)
    
    # Messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message_text TEXT,
            response_text TEXT,
            intent TEXT,
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized")

def save_user(user_id, username, first_name, last_name):
    """Save or update user in database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO users (id, username, first_name, last_name, joined_at, last_active, message_count)
        VALUES (?, ?, ?, ?, COALESCE((SELECT joined_at FROM users WHERE id = ?), ?), ?, 
                COALESCE((SELECT message_count FROM users WHERE id = ?), 0) + 1)
    """, (user_id, username, first_name, last_name, user_id, datetime.now().isoformat(), 
          datetime.now().isoformat(), user_id))
    
    conn.commit()
    conn.close()

def save_message(user_id, message_text, response_text, intent):
    """Save message to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO messages (user_id, message_text, response_text, intent, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, message_text, response_text, intent, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def detect_intent(message):
    """Detect user intent from message"""
    message_lower = message.lower()
    
    intents = {
        'greeting': ['مرحبا', 'اهلا', 'السلام', 'هاي', 'صباح', 'مساء', 'hello', 'hi'],
        'services': ['خدمات', 'خدمة', 'تقدم', 'توفر', 'services', 'what can you do'],
        'prices': ['سعر', 'تكلفة', 'كم', 'ثمن', 'price', 'cost', 'how much'],
        'payment': ['دفع', 'تحويل', 'فودافون', 'كاش', 'payment', 'pay', 'cash'],
        'delivery': ['متى', 'موعد', 'تسليم', 'وقت', 'when', 'delivery', 'time'],
        'contact': ['تواصل', 'اتصال', 'رقم', 'واتساب', 'contact', 'phone', 'whatsapp'],
        'offer': ['عرض', 'خصم', 'تخفيض', 'offer', 'discount', 'deal'],
        'about': ['عن', 'من انت', 'شركة', 'about', 'who are you', 'company'],
        'help': ['مساعدة', 'مساعد', 'ازاي', 'help', 'how to'],
        'thanks': ['شكر', 'ممتاز', 'رائع', 'thanks', 'thank you', 'great']
    }
    
    for intent, keywords in intents.items():
        if any(keyword in message_lower for keyword in keywords):
            return intent
    
    return 'general'

def get_ai_response(message, intent):
    """Get AI response using Anthropic, OpenAI, Kimi, or Gemini"""
    
    # Try Anthropic first
    if ANTHROPIC_KEY and ANTHROPIC_KEY != 'sk-ant-api03--1Y...mAAA':
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
            
            system_prompt = """أنت مساعد ذكي لشركة Hamed AI المتخصصة في الخدمات الرقمية.
ردودك يجب أن تكون:
- احترافية وودية
- باللغة العربية
- مختصرة ومفيدة
- لا ترفض أي خدمة، بل قدم حلول مخصصة
- استخدم الإيموجي بشكل مناسب
- رقم الواتساب: 01061245527
- فودافون كاش: 01061245527"""
            
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                system=system_prompt,
                messages=[{"role": "user", "content": message}]
            )
            
            return response.content[0].text
        except Exception as e:
            print(f"⚠️  Anthropic error: {e}")
    
    # Try OpenAI as fallback
    if OPENAI_KEY and OPENAI_KEY != 'key_C8KiWEvc7gnmHzxF':
        try:
            import openai
            client = openai.OpenAI(api_key=OPENAI_KEY)
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "أنت مساعد ذكي لشركة Hamed AI. رد احترافي بالعربية."},
                    {"role": "user", "content": message}
                ],
                max_tokens=500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️  OpenAI error: {e}")
    
    # Try Kimi as fallback
    if KIMI_KEY and KIMI_KEY != '':
        try:
            import requests
            response = requests.post(
                "https://api.moonshot.cn/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {KIMI_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "moonshot-v1-8k",
                    "messages": [
                        {"role": "system", "content": "أنت مساعد ذكي لشركة Hamed AI. رد احترافي بالعربية."},
                        {"role": "user", "content": message}
                    ],
                    "max_tokens": 500
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"⚠️  Kimi error: {e}")
    
    # Try Gemini as fallback
    if GEMINI_KEY and GEMINI_KEY != '':
        try:
            import requests
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{
                        "parts": [{
                            "text": f"أنت مساعد ذكي لشركة Hamed AI. رد احترافي بالعربية.\n\nالسؤال: {message}"
                        }]
                    }]
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            print(f"⚠️  Gemini error: {e}")
    
    # Fallback to template responses
    return get_template_response(intent)

def get_template_response(intent):
    """Get template response based on intent"""
    templates = {
        'greeting': f"""👋 أهلاً وسهلاً بك!

يسعدنا تواصلك مع Hamed AI 🤖

نحن هنا لمساعدتك في تحقيق أهدافك الرقمية.

📞 للتواصل:
واتساب: {WHATSAPP}
فودافون كاش: {VODAFONE_CASH}

كيف يمكننا خدمتك اليوم؟""",
        
        'services': """🎯 خدماتنا الاحترافية:

📊 تحليل المواقع - يبدأ من $50
📈 تحسين SEO - يبدأ من $150
✍️ كتابة المحتوى - يبدأ من $15/مقال
🎨 التصميم الجرافيكي - يبدأ من $30
📱 إدارة السوشيال ميديا - يبدأ من $200/شهر
💻 تطوير المواقع - حسب المشروع
🤖 أنظمة AI مخصصة - حسب المتطلبات

✅ نقدم حلول مخصصة لكل عميل
💎 جودة عالية وأسعار تنافسية

أي خدمة تهمك؟""",
        
        'prices': """💰 أسعارنا التنافسية:

📊 تحليل المواقع: $50-100
📈 تحسين SEO: $150-300
✍️ كتابة المحتوى: $15-50/مقال
🎨 تصميم شعار: $30-100
📱 إدارة سوشيال: $200-500/شهر
💻 موقع كامل: $500-2000

💎 خصم 20% للعملاء الجدد
🎁 استشارة مجانية

هل تريد تفاصيل أكثر عن خدمة معينة؟""",
        
        'payment': f"""💳 طرق الدفع المتاحة:

📱 فودافون كاش: {VODAFONE_CASH}
💳 تحويل بنكي
🏦 PayPal (للدول الدولي)

📋 خطوات الدفع:
1. تأكيد الطلب
2. إرسال تفاصيل الدفع
3. تأكيد الاستلام
4. بدء العمل فوراً

✅ آمن وشفاف 100%""",
        
        'delivery': """⏱️ مواعيد التسليم:

📊 تحليل المواقع: 2-3 أيام
📈 تحسين SEO: 30 يوم
✍️ كتابة المحتوى: 3-7 أيام
🎨 التصميم: 3-5 أيام
💻 موقع كامل: 7-30 يوم

✅ نلتزم بالمواعيد
🔄 تحديثات دورية
📞 دعم مستمر

هل لديك موعد محدد؟""",
        
        'contact': f"""📞 معلومات التواصل:

📱 واتساب: {WHATSAPP}
💳 فودافون كاش: {VODAFONE_CASH}
🌐 الموقع: hamed-ai.com

⏰ متاحين 24/7
💬 رد سريع على جميع الرسائل

تواصل معنا الآن!""",
        
        'offer': """🎁 عروض خاصة:

✨ خصم 20% على أول خدمة
🎁 استشارة مجانية
💎 باقات مخفضة للخدمات المتعددة
🚀 عروض شهرية حصرية

⏰ العروض محدودة
📞 تواصل الآن للاستفادة

أي عرض يهمك؟""",
        
        'about': """🤖 عن Hamed AI:

نحن شركة متخصصة في الخدمات الرقمية والذكاء الاصطناعي.

🎯 رؤيتنا: تمكين الشركات من النمو رقمياً
💡 مهمتنا: تقديم حلول ذكية بأسعار مناسبة
⭐ قيمنا: الجودة، الاحترافية، الابتكار

📊 أنجزنا +500 مشروع
👥 +200 عميل راضي
🌍 نخدم العملاء في الشرق الأوسط

نحن هنا لمساعدتك!""",
        
        'help': """🆘 كيف يمكننا مساعدتك؟

📋 الأوامر المتاحة:
/start - بدء المحادثة
/services - قائمة الخدمات
/prices - الأسعار
/contact - معلومات التواصل
/offer - العروض الخاصة
/about - عن الشركة
/help - المساعدة

💬 أو اكتب سؤالك مباشرة وسنرد عليك فوراً!""",
        
        'thanks': """🙏 شكراً لك!

يسعدنا خدمتك ونتمنى أن نكون عند حسن ظنك.

💎 نحن هنا دائماً لخدمتك
📞 لا تتردد في التواصل لأي استفسار
⭐ رضاك هو هدفنا

نتطلع للتعاون معك! 🚀""",
        
        'general': f"""💬 شكراً لتواصلك!

نحن هنا لمساعدتك في أي خدمة رقمية تحتاجها.

🎯 خدماتنا تشمل:
- تحليل المواقع
- تحسين SEO
- كتابة المحتوى
- التصميم
- إدارة السوشيال ميديا
- تطوير المواقع
- أنظمة AI

📞 للتواصل السريع:
واتساب: {WHATSAPP}

أخبرنا كيف يمكننا مساعدتك؟"""
    }
    
    return templates.get(intent, templates['general'])

# Try to import telegram
try:
    from telegram import Update, BotCommand
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("⚠️  python-telegram-bot not installed")

# Bot command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    save_user(user.id, user.username, user.first_name, user.last_name)
    
    response = get_template_response('greeting')
    await update.message.reply_text(response)
    
    save_message(user.id, '/start', response, 'greeting')
    print(f"✅ User {user.username} started bot")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    response = get_template_response('help')
    await update.message.reply_text(response)

async def services_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /services command"""
    response = get_template_response('services')
    await update.message.reply_text(response)

async def prices_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /prices command"""
    response = get_template_response('prices')
    await update.message.reply_text(response)

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /contact command"""
    response = get_template_response('contact')
    await update.message.reply_text(response)

async def offer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /offer command"""
    response = get_template_response('offer')
    await update.message.reply_text(response)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command"""
    response = get_template_response('about')
    await update.message.reply_text(response)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all text messages"""
    user = update.effective_user
    message_text = update.message.text
    
    # Save user
    save_user(user.id, user.username, user.first_name, user.last_name)
    
    # Detect intent
    intent = detect_intent(message_text)
    
    # Get AI response
    response = get_ai_response(message_text, intent)
    
    # Send response
    await update.message.reply_text(response)
    
    # Save message
    save_message(user.id, message_text, response, intent)
    
    print(f"✅ Message from {user.username}: {message_text[:50]}...")

def main():
    """Main bot function"""
    if not TELEGRAM_AVAILABLE:
        print("❌ Cannot start bot: python-telegram-bot not installed")
        print("📦 Install with: pip install python-telegram-bot")
        return
    
    if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ Telegram token not configured")
        return
    
    print("\n" + "="*60)
    print("🤖 Hamed AI Telegram Bot")
    print("="*60)
    print(f"✅ Bot Token: {TELEGRAM_TOKEN[:20]}...")
    print(f"✅ Anthropic API: {'✅ Configured' if ANTHROPIC_KEY and ANTHROPIC_KEY != 'sk-ant-api03--1Y...mAAA' else '❌ Not configured'}")
    print(f"✅ OpenAI API: {'✅ Configured' if OPENAI_KEY and OPENAI_KEY != 'key_C8KiWEvc7gnmHzxF' else '❌ Not configured'}")
    print(f"✅ WhatsApp: {WHATSAPP}")
    print(f"✅ Vodafone Cash: {VODAFONE_CASH}")
    print("="*60)
    print("\n🚀 Bot is running 24/7!")
    print("📱 Test it on Telegram: @hamed_ai_bot")
    print("⏹️  Press Ctrl+C to stop\n")
    
    # Initialize database
    init_database()
    
    # Create application
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("services", services_command))
    app.add_handler(CommandHandler("prices", prices_command))
    app.add_handler(CommandHandler("contact", contact_command))
    app.add_handler(CommandHandler("offer", offer_command))
    app.add_handler(CommandHandler("about", about_command))
    
    # Add message handler for all text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start bot
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
