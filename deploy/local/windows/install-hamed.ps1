$ErrorActionPreference = 'Stop'

Write-Host 'Hamed AI - Local Server Setup' -ForegroundColor Cyan
# windows -> local -> deploy -> repository root
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
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
  if (Test-Path '.env.example') {
    Copy-Item '.env.example' '.env'
  } else {
    New-Item '.env' -ItemType File | Out-Null
  }
}

Write-Host 'Local environment prepared.' -ForegroundColor Green
Write-Host 'Start with deploy\local\windows\start-hamed.bat'
