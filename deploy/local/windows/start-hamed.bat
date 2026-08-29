@echo off
setlocal
cd /d "%~dp0\..\..\.."
if not exist .venv\Scripts\python.exe (
  echo Hamed is not installed. Run deploy\local\windows\install-hamed.ps1 first.
  pause
  exit /b 1
)
call .venv\Scripts\activate.bat
if exist local_server.py (
  python local_server.py
) else (
  echo Could not find local_server.py.
  pause
  exit /b 1
)
