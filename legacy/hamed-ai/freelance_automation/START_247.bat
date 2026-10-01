@echo off
chcp 65001 >nul
title 🤖 Freelance Automation - 24/7 Service
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║         🤖 Freelance Automation 24/7 Service              ║
echo ║         Running Continuously...                           ║
echo ║                                                           ║
echo ║   ✓ Monitors platforms automatically                      ║
echo ║   ✓ Processes orders with AI                              ║
echo ║   ✓ Delivers to clients                                   ║
echo ║   ✓ Tracks revenue 24/7                                   ║
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

:: Check if .env exists
if not exist ".env" (
    echo ⚠️  .env file not found!
    echo.
    echo Creating .env from template...
    copy .env.example .env >nul
    echo.
    echo ⚠️  IMPORTANT: Edit .env file and add your AI API keys!
    echo.
    echo Press any key to open .env file...
    pause >nul
    start notepad .env
    echo.
    echo After adding your API keys, run START_247.bat again.
    pause
    exit /b 0
)

:: Validate configuration
echo 🔍 Validating configuration...
python -c "from core.config import Config; errors = Config.validate(); exit(1 if errors else 0)"
if %errorlevel% neq 0 (
    echo.
    echo ❌ Configuration validation failed!
    echo Please check your .env file.
    pause
    exit /b 1
)

echo ✓ Configuration valid
echo.

:: Check if already running
tasklist /FI "WINDOWTITLE eq *24/7 Service*" 2>NUL | find /I /N "cmd.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ⚠️  Service appears to be already running!
    echo.
    set /p choice="Do you want to restart it? (y/n): "
    if /i "%choice%"=="y" (
        taskkill /FI "WINDOWTITLE eq *24/7 Service*" /T /F >nul 2>&1
        timeout /t 2 /nobreak >nul
    ) else (
        exit /b 0
    )
)

echo 🚀 Starting 24/7 service...
echo.
echo The service will run continuously in this window.
echo Press Ctrl+C to stop the service.
echo.
echo ═══════════════════════════════════════════════════════════
echo.

:: Start the service
python service_247.py

:: If service stops, offer to restart
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo Service stopped.
echo.
set /p restart="Restart service? (y/n): "
if /i "%restart%"=="y" (
    echo.
    echo Restarting...
    timeout /t 2 /nobreak >nul
    "%~f0"
) else (
    echo.
    echo Goodbye!
    timeout /t 2 /nobreak >nul
)
