@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo              HAMED AI - STARTUP
echo ============================================

where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.11+ and try again.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo [1/3] Creating virtual environment...
  python -m venv .venv
  if errorlevel 1 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
  )
)

echo [2/3] Installing/updating dependencies...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
  echo Failed to install dependencies.
  pause
  exit /b 1
)

echo [3/3] Starting Hamed AI...
echo.
echo Dashboard: http://127.0.0.1:8000/dashboard
echo API docs:  http://127.0.0.1:8000/docs
echo Health:    http://127.0.0.1:8000/health
echo.
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000

endlocal
