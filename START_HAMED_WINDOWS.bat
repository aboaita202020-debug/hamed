@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title HAMED AI - WINDOWS 7 START
echo ============================================
echo       HAMED AI - START WITH DIAGNOSTICS
echo ============================================
echo.
set "LOG=%~dp0hamed_start.log"
echo [%date% %time%] Starting Hamed>>"%LOG%"
echo [1] Checking Python...
where python >nul 2>nul
if errorlevel 1 goto NO_PYTHON
python --version
if errorlevel 1 goto NO_PYTHON

echo [2] Starting Windows 7 compatibility server...
if not exist "%~dp0win7_server.py" goto NO_SERVER
echo Dashboard: http://127.0.0.1:8000/dashboard
echo Health:    http://127.0.0.1:8000/health
echo.
echo IMPORTANT: keep this black window open while Hamed is running.
echo Press CTRL+C to stop Hamed.
echo.
python "%~dp0win7_server.py" >>"%LOG%" 2>&1
set "ERR=%ERRORLEVEL%"
echo.
if "%ERR%"=="0" goto END
echo Hamed stopped with error code %ERR%.
echo See the log file: %LOG%
echo.
echo The window will remain open so you can read the error.
pause
goto END

:NO_PYTHON
echo.
echo ERROR: Python was not found in PATH.
echo Windows 7 needs Python 3.8.x.
echo Download: https://www.python.org/downloads/release/python-3810/
pause
goto END

:NO_SERVER
echo.
echo ERROR: win7_server.py is missing from this folder.
pause
goto END

:END
endlocal
