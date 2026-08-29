$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

Write-Host '============================================'
Write-Host '           HAMED AI - STARTUP'
Write-Host '============================================'

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host 'Python was not found. Install Python 3.11+ and try again.' -ForegroundColor Red
    exit 1
}

if (-not (Test-Path '.venv\Scripts\python.exe')) {
    Write-Host '[1/3] Creating virtual environment...'
    python -m venv .venv
}

Write-Host '[2/3] Installing/updating dependencies...'
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host '[3/3] Starting Hamed AI...'
Write-Host 'Dashboard: http://127.0.0.1:8000/dashboard'
Write-Host 'API docs:  http://127.0.0.1:8000/docs'
Write-Host 'Health:    http://127.0.0.1:8000/health'

& .venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000
