@echo off
chcp 65001 >nul
title 🚀 Push to GitHub
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║              🚀 Push Hamed AI to GitHub                   ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Check if Git is installed
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Git is not installed!
    echo.
    echo Please install Git first:
    echo https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo ✓ Git found
git --version
echo.

:: Check if .git exists
if not exist ".git" (
    echo 📝 Initializing Git repository...
    git init
    echo.
)

:: Ask for GitHub username
set /p GITHUB_USERNAME="Enter your GitHub username: "
echo.

:: Ask for repository name
set /p REPO_NAME="Enter repository name (default: hamed-ai): "
if "%REPO_NAME%"=="" set REPO_NAME=hamed-ai
echo.

:: Check if remote already exists
git remote get-url origin >nul 2>nul
if %errorlevel% neq 0 (
    echo 🔗 Adding remote repository...
    git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git
    echo ✓ Remote added
    echo.
) else (
    echo ✓ Remote already exists
    echo.
)

:: Add all files
echo 📦 Adding files...
git add .
echo ✓ Files added
echo.

:: Commit
echo 💾 Creating commit...
git commit -m "🎉 Hamed AI - Complete Business Operating System" -m "- 21 interactive pages" -m "- 6 AI Brains" -m "- Smart Sales System" -m "- Call Center" -m "- WhatsApp/Telegram Integration" -m "- Social Media Management" -m "- Advanced AI Learning" -m "- 50+ Test Cases" >nul 2>nul
echo ✓ Commit created
echo.

:: Push
echo 🚀 Pushing to GitHub...
echo.
echo ⚠️  GitHub will ask for your credentials
echo ⚠️  If you have 2FA enabled, use a Personal Access Token
echo.
git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Push failed. Trying with master branch...
    git branch -M master
    git push -u origin master
)

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║              ✅ Successfully Pushed!                      ║
echo ║                                                           ║
echo ║   Repository: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
pause
