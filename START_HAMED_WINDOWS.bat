@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title HAMED AI - WINDOWS 7 START

echo ============================================
echo        HAMED AI - WINDOWS 7 START
echo ============================================
echo.
set "LOG=%~dp0hamed_start.log"
echo [%date% %time%] Starting Hamed>>"%LOG%"

echo [1] Checking Python 3.8...
py -3.8 --version >>"%LOG%" 2>&1
if errorlevel 1 goto NO_PYTHON
py -3.8 --version

echo [2] Checking Hamed server file...
if not exist "%~dp0win7_server.py" goto NO_SERVER

echo [3] Starting Hamed AI...
echo Dashboard: http://127.0.0.1:8000/dashboard
echo Health:    http://127.0.0.1:8000/health
echo.
start "" "http://127.0.0.1:8000/dashboard"
echo Keep this black window open while Hamed is running.
echo Press CTRL+C to stop Hamed.
echo.

py -3.8 "%~dp0win7_server.py" >>"%LOG%" 2>&1
set "ERR=%ERRORLEVEL%"
echo.
if "%ERR%"=="0" goto END
echo Hamed stopped with error code %ERR%.
echo See the log file: %LOG%
echo.
type "%LOG%"
echo.
echo The window will remain open so you can read the error.
pause
goto END

:NO_PYTHON
echo.
echo ERROR: Python 3.8 was not found through py -3.8.
echo Your Hamed Windows 7 launcher requires Python 3.8.x.
echo.
echo Run: py -3.8 --version
pause
goto END

:NO_SERVER
echo.
echo ERROR: win7_server.py is missing from this folder.
pause
goto END

:END
endlocal
