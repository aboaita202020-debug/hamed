@echo off
chcp 65001 >nul
title 🤖 Install 24/7 Service
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║    🤖 Install Freelance Automation as Windows Service     ║
echo ║                                                           ║
echo ║    This will make the service run automatically:          ║
echo ║    • When Windows starts                                  ║
echo ║    • In the background (no window needed)                 ║
echo ║    • 24/7 without manual intervention                     ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Check for admin rights
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  This script requires administrator privileges!
    echo.
    echo Please right-click and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo ✓ Running with administrator privileges
echo.

:: Get current directory
set "SCRIPT_DIR=%~dp0"
set "PYTHON_SCRIPT=%SCRIPT_DIR%service_247.py"

echo 📁 Script location: %SCRIPT_DIR%
echo 📄 Python script: %PYTHON_SCRIPT%
echo.

:: Check if Python script exists
if not exist "%PYTHON_SCRIPT%" (
    echo ❌ Python script not found: %PYTHON_SCRIPT%
    pause
    exit /b 1
)

echo ✓ Python script found
echo.

:: Create scheduled task
echo 📝 Creating Windows scheduled task...
echo.

schtasks /create /tn "FreelanceAutomation247" /tr "python.exe \"%PYTHON_SCRIPT%\"" /sc onlogon /rl highest /f

if %errorlevel% neq 0 (
    echo.
    echo ❌ Failed to create scheduled task!
    echo.
    echo You can create it manually:
    echo 1. Open Task Scheduler
    echo 2. Create Basic Task
    echo 3. Name: FreelanceAutomation247
    echo 4. Trigger: When I log on
    echo 5. Action: Start a program
    echo 6. Program: python.exe
    echo 7. Arguments: "%PYTHON_SCRIPT%"
    echo.
    pause
    exit /b 1
)

echo ✓ Scheduled task created successfully
echo.

:: Start the task now
echo 🚀 Starting service now...
schtasks /run /tn "FreelanceAutomation247"

if %errorlevel% neq 0 (
    echo ⚠️  Could not start task immediately
    echo It will start when you log on next time
) else (
    echo ✓ Service started
)

echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo ✅ Installation complete!
echo.
echo The service will now:
echo   • Run automatically when you log on
echo   • Work 24/7 in the background
echo   • Process orders automatically
echo   • Monitor platforms continuously
echo.
echo To manage the service:
echo   • View: Task Scheduler → FreelanceAutomation247
echo   • Stop: schtasks /end /tn "FreelanceAutomation247"
echo   • Start: schtasks /run /tn "FreelanceAutomation247"
echo   • Delete: schtasks /delete /tn "FreelanceAutomation247" /f
echo.
echo ═══════════════════════════════════════════════════════════
echo.
pause
