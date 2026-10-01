@echo off
chcp 65001 >nul
title 🤖 Freelance Automation System
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║         🤖 Freelance Automation System                    ║
echo ║         6 AI Brains - Local Execution                     ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed!
    echo.
    echo Please install Python 3.8 or newer:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✓ Python found
python --version
echo.

:: Check if .env exists
if not exist ".env" (
    echo 📝 Creating .env file from template...
    copy .env.example .env >nul
    echo.
    echo ⚠️  IMPORTANT: Edit .env file and add your AI API keys!
    echo.
    echo Press any key to open .env file...
    pause >nul
    start notepad .env
    echo.
    echo After adding your API keys, run this script again.
    pause
    exit /b 0
)

:: Validate configuration
echo 🔍 Validating configuration...
python main.py validate
if %errorlevel% neq 0 (
    echo.
    echo ❌ Configuration validation failed!
    echo Please check your .env file.
    pause
    exit /b 1
)

echo.
echo ✓ Configuration valid
echo.

:: Run tests
echo 🧪 Running tests...
python -m unittest discover -s tests -v
if %errorlevel% neq 0 (
    echo.
    echo ❌ Tests failed!
    pause
    exit /b 1
)

echo.
echo ✓ All tests passed
echo.

:: Show menu
:MENU
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo What would you like to do?
echo.
echo 1. Show Dashboard Stats
echo 2. Show AI Brains Status
echo 3. Create New Order
echo 4. Process Order
echo 5. Deliver Order
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto DASHBOARD
if "%choice%"=="2" goto BRAINS
if "%choice%"=="3" goto CREATE
if "%choice%"=="4" goto PROCESS
if "%choice%"=="5" goto DELIVER
if "%choice%"=="6" goto EXIT
echo Invalid choice!
goto MENU

:DASHBOARD
echo.
python main.py dashboard
pause
goto MENU

:BRAINS
echo.
python main.py brains
pause
goto MENU

:CREATE
echo.
set /p platform="Platform (fiverr/upwork/mostaql): "
set /p service="Service (content_writing/translation/data_analysis/code_generation): "
set /p client="Client name: "
set /p description="Description: "
set /p price="Price (USD): "
echo.
python main.py create-order --platform %platform% --service %service% --client "%client%" --description "%description%" --price %price%
pause
goto MENU

:PROCESS
echo.
set /p order_id="Order ID: "
echo.
python main.py process-order %order_id%
pause
goto MENU

:DELIVER
echo.
set /p order_id="Order ID: "
echo.
python main.py deliver-order %order_id%
pause
goto MENU

:EXIT
echo.
echo Goodbye!
timeout /t 2 /nobreak >nul
