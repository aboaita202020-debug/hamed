@echo off
setlocal
cd /d "%~dp0\..\..\.."
if not exist .venv\Scripts\python.exe (
  echo Hamed is not installed. Run deploy\local\windows\install-hamed.ps1 first.
  pause
  exit /b 1
)
call .venv\Scripts\activate.bat
if exist app\main.py (
  python app\main.py
) else if exist main.py (
  python main.py
) else (
  echo Could not find the application entrypoint.
  pause
  exit /b 1
)
