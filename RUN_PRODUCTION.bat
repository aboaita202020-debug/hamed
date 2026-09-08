@echo off
chcp 65001 >nul
title Hamed AI - Production Server
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║              🤖 Hamed AI Dashboard                        ║
echo ║              Production Mode                              ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Check if dist folder exists
if not exist "dist" (
    echo Building production version...
    call npm run build
    echo.
)

:: Install serve if not exists
where serve >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing serve package...
    call npm install -g serve
    echo.
)

:: Open browser
start http://localhost:3000

:: Start production server
echo Starting production server on http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.
serve -s dist -l 3000

pause
