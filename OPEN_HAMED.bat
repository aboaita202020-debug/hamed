@echo off
chcp 65001 >nul
title 🤖 Hamed AI Dashboard
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║              🤖 Hamed AI Dashboard                        ║
echo ║                                                           ║
echo ║    ✅ No installation needed!                             ║
echo ║    ✅ Just double-click and use!                          ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo Opening dashboard in your browser...
echo.

:: Open the standalone HTML file directly
start "" "HAMED_DASHBOARD.html"

echo ✓ Dashboard opened successfully!
echo.
echo You can close this window.
echo.
timeout /t 2 /nobreak >nul
