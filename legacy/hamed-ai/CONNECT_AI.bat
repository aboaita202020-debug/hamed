@echo off
chcp 65001 >nul
title 🤖 Hamed AI - ربط AI APIs
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║         🤖 Hamed AI - ربط AI APIs                         ║
echo ║         اختبار وتشغيل الذكاء الاصطناعي                    ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed!
    echo.
    echo Please install Python 3.8 or newer:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✓ Python found
python --version
echo.

:: Install required packages
echo 📦 Installing required packages...
echo.
pip install python-dotenv anthropic openai requests python-telegram-bot --quiet
if %errorlevel% neq 0 (
    echo ⚠️  Some packages failed to install
    echo Continuing anyway...
    echo.
) else (
    echo ✓ All packages installed successfully
    echo.
)

:: Check .env file
if not exist ".env" (
    echo ❌ .env file not found!
    echo.
    echo Please create .env file with your API keys
    echo.
    pause
    exit /b 1
)

echo ✓ .env file found
echo.

:: Test APIs
echo 🧪 Testing AI APIs...
echo.
python test_apis.py
echo.

:: Ask to start bot
set /p start_bot="هل تريد تشغيل بوت تيليجرام الآن؟ (y/n): "
if /i "%start_bot%"=="y" (
    echo.
    echo 🚀 Starting Telegram Bot...
    echo.
    python bots/telegram_bot.py
) else (
    echo.
    echo ✅ AI APIs ready!
    echo.
    echo To start the bot later, run:
    echo   python bots/telegram_bot.py
    echo.
)

pause
