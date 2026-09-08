@echo off
chcp 65001 >nul
title 🤖 Hamed AI - Complete Business Operating System
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║              🤖 Hamed AI Dashboard                        ║
echo ║         Complete Business Operating System                ║
echo ║                                                           ║
echo ║   ✅ 21 Interactive Pages                                 ║
echo ║   ✅ Advanced AI Brain (6 Brains)                         ║
echo ║   ✅ Smart Sales System                                   ║
echo ║   ✅ Call Center                                          ║
echo ║   ✅ Smart Responses (WhatsApp/Telegram/Voice)            ║
echo ║   ✅ Social Media Management                              ║
echo ║   ✅ Learning System                                      ║
echo ║   ✅ 24/7 Auto-Processing                                 ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Check Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed!
    echo.
    echo Please install Node.js 18 or newer:
    echo https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo ✓ Node.js found
node --version
echo.

:: Check if node_modules exists
if not exist "node_modules" (
    echo 📦 Installing dependencies...
    echo.
    call npm install
    if %errorlevel% neq 0 (
        echo.
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo.
    echo ✓ Dependencies installed successfully
    echo.
)

:: Run tests
echo 🧪 Running tests...
echo.
call npm test
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Some tests failed, but continuing...
    echo.
) else (
    echo.
    echo ✓ All tests passed
    echo.
)

:: Start the development server
echo 🚀 Starting Hamed AI Dashboard...
echo.
echo The dashboard will open automatically in your browser
echo.
echo Press Ctrl+C to stop the server
echo.
echo ═══════════════════════════════════════════════════════════
echo.

:: Open browser after 3 seconds
start "" cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:5173"

:: Start the dev server
call npm run dev

pause
