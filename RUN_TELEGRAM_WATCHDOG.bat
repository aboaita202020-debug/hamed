@echo off
cd /d "D:\hamed agi\hamed-main\hamed-main"
:monitor
wmic process where "CommandLine like '%%scripts\\run_telegram.py%%'" get ProcessId /value | findstr /i "ProcessId" >nul
if not errorlevel 1 (
  timeout /t 5 /nobreak >nul
  goto monitor
)
echo [%date% %time%] Starting Hamed Telegram bot >> telegram_bot.log
.venv\Scripts\python.exe scripts\run_telegram.py >> telegram_bot.log 2>&1
echo [%date% %time%] Bot stopped. Restarting in 3 seconds... >> telegram_bot.log
timeout /t 3 /nobreak >nul
goto monitor
