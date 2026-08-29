@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================
echo          HAMED AI - WINDOWS 7 STARTUP
echo ============================================
echo.

rem Windows 7 requires Python 3.8.x. Newer Python releases do not support Win7.
set "PYTHON_EXE="

py -3.8 -c "import sys; print(sys.version)" >nul 2>nul
if not errorlevel 1 set "PYTHON_EXE=py -3.8"

if not defined PYTHON_EXE (
  python -c "import sys; sys.exit(0 if sys.version_info[:2]==(3,8) else 1)" >nul 2>nul
  if not errorlevel 1 set "PYTHON_EXE=python"
)

if not defined PYTHON_EXE (
  echo Python 3.8.x was not found.
  echo Windows 7 needs Python 3.8.x for this project.
  echo.
  echo Download the official Python 3.8.10 installer:
  echo https://www.python.org/downloads/release/python-3810/
  echo.
  echo Install Python 3.8, then run this file again.
  pause
  exit /b 1
)

echo Using Python:
%PYTHON_EXE% --version

echo.
if not exist ".venv\Scripts\python.exe" (
  echo [1/3] Creating virtual environment...
  %PYTHON_EXE% -m venv .venv
  if errorlevel 1 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
  )
)

echo [2/3] Installing Hamed dependencies...
.venv\Scripts\python.exe -m pip install --upgrade "pip<25"
if errorlevel 1 goto :pip_error
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto :pip_error

echo.
echo [3/3] Starting Hamed AI...
echo.
echo Dashboard: http://127.0.0.1:8000/dashboard
echo API docs:  http://127.0.0.1:8000/docs
echo Health:    http://127.0.0.1:8000/health
echo.
start "Hamed Dashboard" http://127.0.0.1:8000/dashboard
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000

goto :eof

:pip_error
echo.
echo Failed while installing dependencies.
echo Check the internet connection and run this file again.
pause
exit /b 1
