#!/usr/bin/env python3
"""
🔍 فحص بوت تيليجرام - يتأكد من كل حاجة
"""
import os
import sys
from pathlib import Path

print("=" * 70)
print("🔍 فحص بوت تيليجرام")
print("=" * 70)
print()

# 1. فحص Python
print("1️⃣  فحص Python...")
print(f"   ✅ Python {sys.version}")
print()

# 2. فحص .env
print("2️⃣  فحص ملف .env...")
env_path = Path('.env')
if env_path.exists():
    print("   ✅ ملف .env موجود")
    
    # قراءة المفاتيح
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        anthropic = os.getenv('ANTHROPIC_API_KEY', '')
        openai = os.getenv('OPENAI_API_KEY', '')
        kimi = os.getenv('KIMI_API_KEY', '')
        gemini = os.getenv('GEMINI_API_KEY', '')
        
        print(f"   ✅ توكن البوت: {token[:20]}..." if token else "   ❌ توكن البوت غير موجود")
        print(f"   ✅ Anthropic: {anthropic[:20]}..." if anthropic else "   ❌ Anthropic غير موجود")
        print(f"   ✅ OpenAI: {openai[:20]}..." if openai else "   ❌ OpenAI غير موجود")
        print(f"   ✅ Kimi: {kimi[:20]}..." if kimi else "   ❌ Kimi غير موجود")
        print(f"   ✅ Gemini: {gemini[:20]}..." if gemini else "   ❌ Gemini غير موجود")
        
    except ImportError:
        print("   ⚠️  python-dotenv غير مثبت")
        print("   📦 ثبّته بالأمر: pip install python-dotenv")
else:
    print("   ❌ ملف .env غير موجود")
    print("   📝 انسخ .env.example إلى .env وأضف المفاتيح")
print()

# 3. فحص المكتبات
print("3️⃣  فحص المكتبات...")
libraries = {
    'requests': 'HTTP Requests',
    'sqlite3': 'SQLite Database',
    'json': 'JSON Processing'
}

optional_libraries = {
    'telegram': 'Telegram Bot',
    'anthropic': 'Anthropic Claude',
    'openai': 'OpenAI GPT-4',
    'dotenv': 'Environment Variables'
}

for lib, name in libraries.items():
    try:
        __import__(lib)
        print(f"   ✅ {name:30} - مثبت")
    except ImportError:
        print(f"   ❌ {name:30} - غير مثبت")

print()
print("   المكتبات الاختيارية:")
for lib, name in optional_libraries.items():
    try:
        __import__(lib)
        print(f"   ✅ {name:30} - مثبت")
    except ImportError:
        print(f"   ⚠️  {name:30} - اختياري")
print()

# 4. فحص توكن البوت
print("4️⃣  فحص توكن البوت...")
if 'token' in locals() and token:
    try:
        import requests
        response = requests.get(f'https://api.telegram.org/bot{token}/getMe', timeout=10)
        
        if response.status_code == 200:
            bot_info = response.json()['result']
            print(f"   ✅ البوت متصل!")
            print(f"   📱 اسم البوت: @{bot_info['username']}")
            print(f"   🤖 معرف البوت: {bot_info['id']}")
            print(f"   📝 الوصف: {bot_info.get('first_name', 'N/A')}")
        else:
            print(f"   ❌ البوت غير متصل")
            print(f"   ⚠️  خطأ: {response.status_code}")
            print(f"   💡 تأكد إن التوكن صحيح")
    except Exception as e:
        print(f"   ❌ فشل الاتصال: {e}")
else:
    print("   ❌ التوكن غير موجود")
print()

# 5. فحص ملفات البوت
print("5️⃣  فحص ملفات البوت...")
bot_files = [
    'bots/telegram_bot.py',
    'bots/__init__.py'
]

for file in bot_files:
    if Path(file).exists():
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} غير موجود")
print()

# 6. ملخص
print("=" * 70)
print("📊 ملخص الحالة")
print("=" * 70)
print()

issues = []

if 'token' not in locals() or not token:
    issues.append("❌ توكن البوت غير موجود في .env")

if not Path('.env').exists():
    issues.append("❌ ملف .env غير موجود")

try:
    import telegram
except ImportError:
    issues.append("⚠️  مكتبة python-telegram-bot غير مثبتة")

if issues:
    print("🔴 المشاكل:")
    for issue in issues:
        print(f"   {issue}")
    print()
    print("🔧 الحل:")
    print("   1. تأكد إن ملف .env موجود وفيه المفاتيح")
    print("   2. ثبّت المكتبات: pip install python-telegram-bot python-dotenv")
    print("   3. تأكد إن التوكن صحيح")
    print("   4. شغّل البوت: python bots/telegram_bot.py")
else:
    print("✅ كل حاجة تمام!")
    print()
    print("🚀 شغّل البوت:")
    print("   python bots/telegram_bot.py")
    print()
    print("📱 جرب البوت في تيليجرام:")
    print("   1. افتح تيليجرام")
    print("   2. ابحث عن: @hamed_ai_bot")
    print("   3. ابعت: /start")

print()
print("=" * 70)
