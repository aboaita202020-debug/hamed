@echo off
chcp 65001 >nul
title Hamed AI - Open Dashboard
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║              🤖 Hamed AI Dashboard                        ║
echo ║              Opening in Browser                           ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Check if dist folder exists
if not exist "dist\index.html" (
    echo Building project first...
    call npm run build
    echo.
)

:: Open the built index.html directly in browser
echo Opening dashboard in your default browser...
echo.
start "" "dist\index.html"

echo ✓ Dashboard opened successfully!
echo.
echo You can close this window.
echo.
timeout /t 3 /nobreak >nul
