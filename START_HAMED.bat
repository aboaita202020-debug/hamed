@echo off
setlocal
cd /d "%~dp0"
title Hamed AI - Launcher

echo ========================================
echo          HAMED AI - STARTING
echo ========================================
echo.

echo [1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Install Python, then run this file again.
    pause
    exit /b 1
)

echo [2/3] Starting Hamed AI...
echo.
start "Hamed AI Server" cmd /k "cd /d "%~dp0" && python -m app.main"

timeout /t 3 /nobreak >nul

echo [3/3] Opening Hamed Dashboard...
start "" "http://127.0.0.1:8000/dashboard"

echo.
echo Hamed AI is starting.
echo Dashboard: http://127.0.0.1:8000/dashboard
echo.
echo Keep the Hamed AI Server window open while using Hamed.
echo You can close this launcher window.
endlocal
