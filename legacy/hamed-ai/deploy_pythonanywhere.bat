@echo off
chcp 65001 >nul
title 🚀 Deploy to PythonAnywhere
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║         🚀 Deploy Hamed AI to PythonAnywhere              ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Check if project is on GitHub
if not exist ".git" (
    echo ❌ Project is not on GitHub yet!
    echo.
    echo Please run push_to_github.bat first
    echo.
    pause
    exit /b 1
)

echo ✓ Project is on GitHub
echo.

:: Ask for PythonAnywhere username
set /p PA_USERNAME="Enter your PythonAnywhere username: "
echo.

:: Ask for GitHub repository URL
set /p GITHUB_URL="Enter your GitHub repository URL (e.g., https://github.com/username/hamed-ai.git): "
echo.

echo ═══════════════════════════════════════════════════════════
echo.
echo 📋 Follow these steps on PythonAnywhere:
echo.
echo 1. Go to https://www.pythonanywhere.com/ and login
echo.
echo 2. Open a Bash console (Click "Bash" button)
echo.
echo 3. Clone your repository:
echo    git clone %GITHUB_URL%
echo.
echo 4. Navigate to the project:
echo    cd hamed-ai
echo.
echo 5. Create a virtual environment:
echo    mkvirtualenv --python=/usr/bin/python3.10 hamed-env
echo.
echo 6. Install requirements:
echo    pip install -r requirements.txt
echo.
echo 7. Set up environment variables:
echo    nano .env
echo    (Add your API keys and configuration)
echo.
echo 8. Go to Web tab in PythonAnywhere
echo.
echo 9. Click "Add a new web app"
echo.
echo 10. Select "Manual configuration" → "Python 3.10"
echo.
echo 11. Set Source code to: /home/%PA_USERNAME%/hamed-ai
echo.
echo 12. Set Working directory to: /home/%PA_USERNAME%/hamed-ai
echo.
echo 13. Edit WSGI configuration file:
echo     - Delete all content
echo     - Copy content from pythonanywhere/wsgi.py
echo     - Replace YOUR_USERNAME with: %PA_USERNAME%
echo.
echo 14. Click "Reload" button
echo.
echo 15. Your app is live at:
echo     https://%PA_USERNAME%.pythonanywhere.com
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo ✅ After deployment, your dashboard will be available at:
echo    https://%PA_USERNAME%.pythonanywhere.com
echo.
echo 📞 Contact:
echo    WhatsApp: 01061245527
echo    Vodafone Cash: 01061245527
echo.
pause
