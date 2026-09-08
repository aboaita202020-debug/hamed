@echo off
chcp 65001 >nul
title 🔧 إصلاح بوت تيليجرام
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║         🔧 إصلاح وتشغيل بوت تيليجرام                      ║
echo ║         فحص شامل وإصلاح تلقائي                            ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: الانتقال لمجلد freelance_automation
cd freelance_automation

:: 1. فحص Python
echo 1️⃣  فحص Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python غير مثبت!
    echo.
    echo حمّل Python من: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo ✅ Python موجود
echo.

:: 2. تثبيت المكتبات
echo 2️⃣  تثبيت المكتبات المطلوبة...
echo.
pip install python-dotenv requests python-telegram-bot --quiet
if %errorlevel% neq 0 (
    echo ⚠️  بعض المكتبات فشلت في التثبيت
    echo.
) else (
    echo ✅ كل المكتبات مثبتة
    echo.
)

:: 3. فحص .env
echo 3️⃣  فحص ملف .env...
if not exist ".env" (
    echo ❌ ملف .env غير موجود!
    echo.
    echo 📝 إنشاء ملف .env من .env.example...
    copy .env.example .env >nul
    echo ✅ تم إنشاء .env
    echo.
    echo ⚠️  مهم: افتح ملف .env وأضف المفاتيح الحقيقية
    echo.
    notepad .env
    pause
    exit /b 1
)
echo ✅ ملف .env موجود
echo.

:: 4. فحص البوت
echo 4️⃣  فحص حالة البوت...
python check_bot.py
echo.

:: 5. تشغيل البوت
echo 5️⃣  تشغيل البوت...
echo.
echo 🚀 البوت هيشتغل دلوقتي...
echo 📱 جرب البوت في تيليجرام: @hamed_ai_bot
echo 💬 ابعت: /start
echo.
echo ═══════════════════════════════════════════════════════════
echo.

python bots/telegram_bot.py

pause
