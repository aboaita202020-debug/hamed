@echo off
chcp 65001 >nul
title 🤖 Service Status
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║         🤖 Freelance Automation - Service Status          ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Check if scheduled task exists
schtasks /query /tn "FreelanceAutomation247" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Service is NOT installed as Windows task
    echo.
    echo To install: Run INSTALL_SERVICE.bat as administrator
    echo.
) else (
    echo ✓ Service is installed as Windows task
    echo.
    
    :: Check if running
    schtasks /query /tn "FreelanceAutomation247" /fo LIST | findstr /i "Running" >nul
    if %errorlevel% equ 0 (
        echo ✅ Service is RUNNING
    ) else (
        echo ❌ Service is NOT running
    )
    echo.
    
    :: Show task details
    echo 📋 Task Details:
    schtasks /query /tn "FreelanceAutomation247" /fo LIST
    echo.
)

:: Check for running Python processes
echo 🔍 Checking for running Python processes...
tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq *24/7*" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ Found running 24/7 service process
) else (
    echo ⚠️  No running 24/7 service process found
)
echo.

:: Show database stats
echo 📊 Database Statistics:
python -c "from core.database import Database; db = Database(); pending = db.fetch_one('SELECT COUNT(*) as count FROM orders WHERE status = ^\"pending^\"'); in_progress = db.fetch_one('SELECT COUNT(*) as count FROM orders WHERE status = ^\"in_progress^\"'); completed = db.fetch_one('SELECT COUNT(*) as count FROM orders WHERE status = ^\"completed^\"'); revenue = db.get_revenue_summary(days=1); print(f'  Pending Orders: {pending[\"count\"]}'); print(f'  In Progress: {in_progress[\"count\"]}'); print(f'  Completed: {completed[\"count\"]}'); print(f'  Revenue (24h): ${revenue[\"total_revenue\"]:.2f}')" 2>nul

if %errorlevel% neq 0 (
    echo ⚠️  Could not retrieve database stats
)
echo.

echo ═══════════════════════════════════════════════════════════
echo.
pause
