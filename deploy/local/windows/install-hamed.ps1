$ErrorActionPreference = 'Stop'

Write-Host 'Hamed AI - Local Server Setup' -ForegroundColor Cyan
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $root

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  throw 'Python 3 is required. Install Python 3.11+ and enable Add Python to PATH.'
}

python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
if (Test-Path 'requirements.txt') {
  & .\.venv\Scripts\python.exe -m pip install -r requirements.txt
}

if (-not (Test-Path '.env')) {
  if (Test-Path 'deploy\oracle\hamed.env.example') {
    Copy-Item 'deploy\oracle\hamed.env.example' '.env'
  } else {
    New-Item '.env' -ItemType File | Out-Null
  }
}

Write-Host 'Local environment prepared.' -ForegroundColor Green
Write-Host 'Edit .env and add credentials only if you want external AI/voice features.'
Write-Host 'For a free local test, keep voice/paid integrations disabled.'
