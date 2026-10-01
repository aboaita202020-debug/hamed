@echo off
chcp 65001 >nul
title Hamed AI - Quick Start
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║              🤖 Hamed AI Dashboard                        ║
echo ║         Multi-Agent Business Operating System             ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo Starting in 3 seconds...
echo.

timeout /t 3 /nobreak >nul

:: Check if node_modules exists, if not install
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
    echo.
)

:: Open browser
start http://localhost:5173

:: Start server
call npm run dev

pause
