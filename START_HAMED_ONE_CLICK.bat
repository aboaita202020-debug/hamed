@echo off
setlocal
cd /d "%~dp0"
title Hamed AI - One Click Launcher

echo ========================================
echo        HAMED AI - ONE CLICK START
echo ========================================
echo.

if not exist ".env" (
    echo ERROR: .env is missing.
    echo Create .env from .env.example and add your keys once.
    echo.
    pause
    exit /b 1
)

echo Checking Python syntax...
python -m compileall app >nul
if errorlevel 1 (
    echo ERROR: Python compile check failed.
    echo Run the project diagnostics before starting.
    echo.
    pause
    exit /b 1
)

echo Starting Hamed AI...
echo Keep this window open while Hamed is running.
echo.
python bot.py

echo.
echo Hamed stopped or exited. The window is intentionally kept open so errors can be read.
pause
endlocal
