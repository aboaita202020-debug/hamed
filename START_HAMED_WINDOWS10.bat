@echo off
setlocal EnableExtensions EnableDelayedExpansion
chcp 65001 >nul
cd /d "%~dp0"
title HAMED AI - Windows 10 64-bit
color 0A

echo ============================================================
echo                 HAMED AI - WINDOWS 10
echo ============================================================
echo.

REM ---- Python -------------------------------------------------
set "PYTHON="
where py >nul 2>nul
if %errorlevel%==0 (
    py -3.11 -c "import sys; print(sys.version)" >nul 2>nul
    if !errorlevel!==0 set "PYTHON=py -3.11"
)
if not defined PYTHON (
    where python >nul 2>nul
    if !errorlevel!==0 set "PYTHON=python"
)
if not defined PYTHON (
    echo [ERROR] Python 3.11 is required.
    echo Install Python 3.11 x64, then run this file again.
    pause
    exit /b 1
)
echo [OK] Python detected.

REM ---- Node.js ------------------------------------------------
where node >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Node.js 18+ is required for the dashboard.
    echo Install Node.js 18 or newer, then run this file again.
    pause
    exit /b 1
)
echo [OK] Node.js detected.

REM ---- Python virtual environment -----------------------------
if not exist ".venv\Scripts\python.exe" (
    echo [SETUP] Creating Python virtual environment...
    %PYTHON% -m venv .venv
    if errorlevel 1 goto :python_error
)
call ".venv\Scripts\activate.bat"

if not exist ".venv\.hamed_deps_ok" (
    echo [SETUP] Installing Python dependencies...
    python -m pip install --upgrade pip
    if errorlevel 1 goto :python_error
    python -m pip install -r requirements.txt
    if errorlevel 1 goto :python_error
    type nul > ".venv\.hamed_deps_ok"
)

REM ---- Frontend dependencies ----------------------------------
if not exist "node_modules" (
    echo [SETUP] Installing dashboard dependencies...
    call npm install
    if errorlevel 1 goto :node_error
)

REM ---- Local free AI brain ------------------------------------
where ollama >nul 2>nul
if errorlevel 1 (
    echo.
    echo [NOTICE] Ollama is not installed.
    echo Hamed will start, but the keyless local AI brain will not answer
    echo until Ollama is installed and a local model is available.
    echo Recommended model: llama3.2:3b
    echo.
) else (
    echo [OK] Ollama detected.
    tasklist /FI "IMAGENAME eq ollama.exe" 2>nul | find /I "ollama.exe" >nul
    if errorlevel 1 (
        echo [SETUP] Starting Ollama...
        start "Hamed Ollama" /min cmd /c "ollama serve"
        timeout /t 4 /nobreak >nul
    )
    ollama list 2>nul | findstr /I "llama3.2:3b" >nul
    if errorlevel 1 (
        echo [SETUP] Downloading local free model llama3.2:3b...
        ollama pull llama3.2:3b
        if errorlevel 1 echo [NOTICE] Model download failed; Hamed can still use configured API brains.
    )
)

REM ---- Start backend ------------------------------------------
echo.
echo [START] Hamed backend on http://127.0.0.1:8000
start "Hamed Backend" cmd /k "cd /d "%~dp0" ^&^& call .venv\Scripts\activate.bat ^&^& python scripts\run_server.py"

timeout /t 4 /nobreak >nul

REM ---- Start frontend -----------------------------------------
echo [START] Hamed dashboard on http://127.0.0.1:5173
start "Hamed Dashboard" cmd /k "cd /d "%~dp0" ^&^& npm run dev -- --host 127.0.0.1"

timeout /t 5 /nobreak >nul
start "" "http://127.0.0.1:5173"

echo.
echo ============================================================
echo Hamed is starting.
echo Dashboard: http://127.0.0.1:5173
echo Backend:   http://127.0.0.1:8000/health
echo.
echo Close the two Hamed command windows to stop the system.
echo ============================================================
echo.
pause
exit /b 0

:python_error
echo [ERROR] Python setup failed. See the message above.
pause
exit /b 1

:node_error
echo [ERROR] Node.js dependency installation failed.
pause
exit /b 1
