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
    start "Hamed Backend" cmd /k "cd /d "%~dp0" ^&^& .venv\Scripts\python.exe scripts\run_server.py"
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

REM ---- Frontend ------------------------------------------------
echo [START] Checking Hamed dashboard on http://127.0.0.1:5173
curl -s http://127.0.0.1:5173 >nul 2>nul
if errorlevel 1 (
    start "Hamed Dashboard" cmd /k "cd /d "%~dp0" ^&^& npm run dev -- --host 127.0.0.1"
) else (
    echo [OK] Dashboard is already running.
)

timeout /t 5 /nobreak >nul
start "" "http://127.0.0.1:5173"

echo.
echo ============================================================
echo HAMED AI IS RUNNING
 echo Dashboard: http://127.0.0.1:5173
 echo Backend:   http://127.0.0.1:8000/health
 echo Chat API:  http://127.0.0.1:8000/chat
 echo ============================================================
echo.
echo This launcher starts backend and dashboard in separate windows.
echo ============================================================
pause
exit /b 0

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
