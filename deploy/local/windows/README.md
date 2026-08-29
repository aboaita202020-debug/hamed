# Hamed AI — Local Windows Server

This mode runs Hamed on your own Windows computer. Your phone does not need to stay online. The computer must remain powered on for Hamed to remain available.

## Requirements

- Windows 10/11 recommended
- Python 3.11+
- Git
- Internet connection for external APIs and learning sources

## Install

Open PowerShell in the repository and run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\deploy\local\windows\install-hamed.ps1
```

## Start

Double-click `deploy\local\windows\start-hamed.bat`, or run it from a terminal.

## Automatic startup

To start Hamed when Windows starts, create a shortcut to `start-hamed.bat` in:

`Win + R` → `shell:startup`

For a more robust always-on setup, run Hamed as a Windows service after confirming the application's production entrypoint.

## Free-first mode

Keep paid integrations disabled while testing. External OpenAI/Twilio services may incur usage charges even though the local server itself is free.

## Security

Never commit `.env`, API keys, Twilio tokens, or customer credentials to GitHub.
