@echo off
chcp 65001 >nul
title 🤖 Stop 24/7 Service
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║         🤖 Stop Freelance Automation Service              ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Check for admin rights
net session >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Running with administrator privileges
    echo.
    
    :: Try to stop scheduled task
    echo 🛑 Stopping scheduled task...
    schtasks /end /tn "FreelanceAutomation247" >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✓ Scheduled task stopped
    ) else (
        echo ⚠️  Scheduled task was not running
    )
    echo.
) else (
    echo ⚠️  Not running as administrator
    echo Some operations may not work
    echo.
)

:: Kill any running Python processes with our service
echo 🛑 Stopping running service processes...
taskkill /FI "WINDOWTITLE eq *24/7 Service*" /T /F >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Service process stopped
) else (
    echo ⚠️  No running service process found
)
echo.

echo ✅ Service stopped
echo.
echo To start again:
echo   • Manual: Run START_247.bat
echo   • Automatic: Service will restart on next login
echo.
pause
