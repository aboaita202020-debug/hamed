@echo off
chcp 65001 >nul
title 🤖 Hamed AI Telegram Bot - Auto Start
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║         🤖 Hamed AI Telegram Bot                          ║
echo ║         Auto-Start from Double-Click                      ║
echo ║                                                           ║
echo ║   ✅ 24/7 Automatic Operation                             ║
echo ║   ✅ AI-Powered Responses (Anthropic + OpenAI)            ║
echo ║   ✅ Smart Intent Detection                               ║
echo ║   ✅ Professional Customer Service                        ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Check Python
echo 🔍 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Python is not installed!
    echo.
    echo 📥 Please install Python 3.8 or newer:
    echo    https://www.python.org/downloads/
    echo.
    echo ⚠️  Important: Check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

python --version
echo ✅ Python found
echo.

:: Navigate to project directory
cd /d "%~dp0freelance_automation"

:: Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
    echo.
)

:: Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

:: Install required packages
echo 📦 Installing required packages...
echo.

:: Check if packages are installed
python -c "import telegram" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📥 Installing python-telegram-bot...
    pip install python-telegram-bot==20.7
    if %errorlevel% neq 0 (
        echo ❌ Failed to install python-telegram-bot
        pause
        exit /b 1
    )
    echo ✅ python-telegram-bot installed
    echo.
)

python -c "import anthropic" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📥 Installing anthropic...
    pip install anthropic==0.39.0
    if %errorlevel% neq 0 (
        echo ⚠️  Failed to install anthropic (optional)
        echo    Bot will use template responses instead
    ) else (
        echo ✅ anthropic installed
        echo.
    )
)

python -c "import openai" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📥 Installing openai...
    pip install openai==1.55.0
    if %errorlevel% neq 0 (
        echo ⚠️  Failed to install openai (optional)
        echo    Bot will use template responses instead
    ) else (
        echo ✅ openai installed
        echo.
    )
)

python -c "import dotenv" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📥 Installing python-dotenv...
    pip install python-dotenv==1.0.0
    if %errorlevel% neq 0 (
        echo ⚠️  Failed to install python-dotenv (optional)
    ) else (
        echo ✅ python-dotenv installed
        echo.
    )
)

echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo 🚀 Starting Telegram Bot...
echo.
echo 📱 Bot will run 24/7 and auto-reply to all messages
echo ⏹️  Press Ctrl+C to stop the bot
echo.
echo ═══════════════════════════════════════════════════════════
echo.

:: Start the bot
python bots/telegram_bot.py

:: If bot stops, offer to restart
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo ⏹️  Bot stopped
echo.
set /p restart="🔄 Restart bot? (y/n): "
if /i "%restart%"=="y" (
    echo.
    echo 🔄 Restarting...
    timeout /t 2 /nobreak >nul
    "%~f0"
) else (
    echo.
    echo 👋 Goodbye!
    timeout /t 2 /nobreak >nul
)
