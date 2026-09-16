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
if exist ".venv\Scripts\python.exe" set "PYTHON=.venv\Scripts\python.exe"
if not defined PYTHON (
    where py >nul 2>nul
    if not errorlevel 1 (
        py -3.11 -c "import sys; print(sys.version)" >nul 2>nul
        if not errorlevel 1 set "PYTHON=py -3.11"
    )
)
if not defined PYTHON (
    where python >nul 2>nul
    if not errorlevel 1 set "PYTHON=python"
)
if not defined PYTHON (
    echo [ERROR] Python 3.11 is required.
    pause
    exit /b 1
)
echo [OK] Python detected: %PYTHON%

REM ---- Node.js ------------------------------------------------
where node >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Node.js 18+ is required for the dashboard.
    pause
    exit /b 1
)
echo [OK] Node.js detected.

REM ---- Python dependencies ------------------------------------
if not exist ".venv\Scripts\python.exe" (
    echo [SETUP] Creating Python virtual environment...
    %PYTHON% -m venv .venv
    if errorlevel 1 goto :python_error
)
if not exist ".venv\.hamed_deps_ok" (
    echo [SETUP] Installing Python dependencies...
    .venv\Scripts\python.exe -m pip install --upgrade pip
    if errorlevel 1 goto :python_error
    .venv\Scripts\python.exe -m pip install -r requirements.txt
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
if not errorlevel 1 (
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
    )
) else (
    echo [NOTICE] Ollama not installed. Hamed can use configured API brains.
)

REM ---- Backend -------------------------------------------------
echo.
echo [START] Checking Hamed backend on http://127.0.0.1:8000
curl -s http://127.0.0.1:8000/health >nul 2>nul
if errorlevel 1 (
    echo [START] Launching Hamed backend...
    start "Hamed Backend" /D "%~dp0" cmd /k ".venv\Scripts\python.exe scripts\run_server.py"
) else (
    echo [OK] Hamed backend is already running.
)

REM Wait for backend readiness without requiring user input.
set /a WAIT=0
:wait_backend
curl -s http://127.0.0.1:8000/health >nul 2>nul
if not errorlevel 1 goto backend_ready
set /a WAIT+=1
if %WAIT% GEQ 20 goto backend_timeout
timeout /t 1 /nobreak >nul
goto wait_backend

:backend_ready
echo [OK] Backend is ready.

REM ---- Autonomous work + learning ------------------------------
echo [START] Checking Hamed autonomous worker on http://127.0.0.1:8010
curl -s http://127.0.0.1:8010/health >nul 2>nul
if errorlevel 1 (
    echo [START] Launching autonomous work and learning loop...
    start "Hamed Autonomous Worker" /D "%~dp0" cmd /k ".venv\Scripts\python.exe scripts\autonomous_worker.py"
) else (
    echo [OK] Autonomous worker is already running.
)

set /a AWAIT=0
:wait_autonomous
curl -s http://127.0.0.1:8010/health >nul 2>nul
if not errorlevel 1 goto autonomous_ready
set /a AWAIT+=1
if %AWAIT% GEQ 20 goto autonomous_timeout
timeout /t 1 /nobreak >nul
goto wait_autonomous

:autonomous_ready
echo [OK] Autonomous worker is ready. Hamed will learn and work continuously.

REM ---- Hamed UI ------------------------------------------------
REM The main Hamed interface is the existing root index.html served by Vite.
REM Keep it on port 3000 so the familiar Hamed UI opens directly.
echo [START] Checking Hamed UI on http://127.0.0.1:3000
curl -s http://127.0.0.1:3000 >nul 2>nul
if errorlevel 1 (
    start "Hamed UI" /D "%~dp0" cmd /k "npm run dev -- --host 127.0.0.1 --port 3000"
) else (
    echo [OK] Hamed UI is already running.
)

REM Wait briefly for Vite, then open the main interface.
set /a UIWAIT=0
:wait_ui
curl -s http://127.0.0.1:3000 >nul 2>nul
if not errorlevel 1 goto ui_ready
set /a UIWAIT+=1
if %UIWAIT% GEQ 20 goto ui_timeout
timeout /t 1 /nobreak >nul
goto wait_ui

:ui_ready
start "" "http://127.0.0.1:3000/"

echo.
echo ============================================================
echo HAMED AI IS RUNNING AND WORKING
echo Main UI:        http://127.0.0.1:3000/
echo Backend:        http://127.0.0.1:8000/health
echo Smart Minds:    http://127.0.0.1:8000/smart-minds
echo Autonomous:     http://127.0.0.1:8010/status
echo Activity log:   data\autonomous_activity.jsonl
echo ============================================================
echo Hamed starts learning immediately, generates business opportunities,
echo records the work, then repeats automatically every 30 minutes.
echo ============================================================
exit /b 0

:ui_timeout
echo [ERROR] Hamed UI did not become ready on port 3000.
echo Check the Hamed UI window for the startup error.
pause
exit /b 1

:autonomous_timeout
echo [ERROR] Autonomous worker did not become ready on port 8010.
echo Check the Hamed Autonomous Worker window for the startup error.
pause
exit /b 1

:backend_timeout
echo [ERROR] Backend did not become ready on port 8000.
echo Check the Hamed Backend window for the startup error.
pause
exit /b 1

:python_error
echo [ERROR] Python setup failed. See the message above.
pause
exit /b 1

:node_error
echo [ERROR] Node.js dependency installation failed.
pause
exit /b 1
