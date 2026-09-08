@echo off
chcp 65001 >nul
title 🚀 Hamed AI - تشغيل كل حاجة
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║         🚀 Hamed AI - تشغيل كل حاجة                      ║
echo ║         دبل كليك وهيشتغل كل شيء تلقائياً                  ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: 1. تثبيت المكتبات
echo 📦 تثبيت المكتبات المطلوبة...
echo.
pip install python-dotenv requests python-telegram-bot --quiet
if %errorlevel% equ 0 (
    echo ✅ المكتبات اتثبتت
) else (
    echo ⚠️  بعض المكتبات فشلت
)
echo.

:: 2. تشغيل البوت في الخلفية
echo 🤖 تشغيل بوت تيليجرام...
start /B cmd /c "cd freelance_automation && python bots/telegram_bot.py"
echo ✅ البوت بيشتغل في الخلفية
echo.

:: 3. فتح الداشبورد
echo 📊 فتح الداشبورد...
timeout /t 2 /nobreak >nul
start "" "dashboard.html"
echo ✅ الداشبورد اتفتح
echo.

:: 4. فتح البوت في تيليجرام
echo 📱 فتح البوت في تيليجرام...
timeout /t 2 /nobreak >nul
start "" "https://t.me/hamed_ai_bot"
echo ✅ البوت اتفتح في تيليجرام
echo.

:: 5. فتح CONTROL_CENTER
echo 🎛️  فتح مركز التحكم...
timeout /t 2 /nobreak >nul
start "" "CONTROL_CENTER.html"
echo ✅ مركز التحكم اتفتح
echo.

echo ═══════════════════════════════════════════════════════════
echo.
echo ✅ كل حاجة شغالة دلوقتي!
echo.
echo 📱 البوت شغال في تيليجرام: @hamed_ai_bot
echo 💬 ابعت: /start
echo.
echo 📊 الداشبورد شغال في المتصفح
echo 🎛️  مركز التحكم شغال
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo ⚠️  لا تقفل النافذة دي!
echo    البوت بيشتغل في الخلفية
echo.
echo    لو عايز توقف البوت:
echo    اضغط Ctrl+C
echo.
echo ═══════════════════════════════════════════════════════════
echo.

:: Keep window open
pause
