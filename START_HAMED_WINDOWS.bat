@echo off
setlocal EnableExtensions
cd /d "%~dp0"

title HAMED AI - WINDOWS 7 START

echo ============================================
echo          HAMED AI - WINDOWS 7 START
 echo ============================================

echo Checking Python...
where python >nul 2>nul
if errorlevel 1 (
  echo.
  echo Python is not installed or is not in PATH.
  echo Install Python 3.8.10 for Windows 7, then run this file again.
  echo.
  echo Download: https://www.python.org/downloads/release/python-3810/
  pause
  exit /b 1
)

python --version

echo.
echo Starting Windows 7 compatibility server...
echo Dashboard: http://127.0.0.1:8000/dashboard
echo Health:    http://127.0.0.1:8000/health
echo.
echo IMPORTANT: keep this black window open while Hamed is running.
echo Press CTRL+C to stop Hamed.
echo.
python win7_server.py

if errorlevel 1 (
  echo.
  echo Hamed stopped because of an error.
  pause
)
endlocal
