@echo off
chcp 65001 >nul
title 🤖 Telegram Bot - Hamed AI
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║         🤖 Hamed AI - Telegram Bot                        ║
echo ║         Running 24/7 Automatically                        ║
echo ║                                                           ║
echo ║   ✅ Auto-replies to all messages                         ║
echo ║   ✅ Professional responses                               ║
echo ║   ✅ Smart intent detection                               ║
echo ║   ✅ Customer support 24/7                                ║
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

:: Check if python-telegram-bot is installed
python -c "import telegram" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing python-telegram-bot...
    echo.
    pip install python-telegram-bot
    if %errorlevel% neq 0 (
        echo.
        echo ⚠️  Failed to install python-telegram-bot
        echo Running in simulation mode...
        echo.
    ) else (
        echo.
        echo ✓ python-telegram-bot installed successfully
        echo.
    )
)

:: Check if .env exists
if not exist ".env" (
    echo 📝 Creating .env file...
    copy .env.example .env >nul
    echo ✓ .env file created
    echo.
)

echo 🚀 Starting Telegram Bot...
echo.
echo The bot will run 24/7 and auto-reply to all messages.
echo Press Ctrl+C to stop the bot.
echo.
echo ═══════════════════════════════════════════════════════════
echo.

:: Start the bot
cd freelance_automation
python bots/telegram_bot.py

pause
