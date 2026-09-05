#!/data/data/com.termux/files/usr/bin/bash

# Hamed AI - Android/Termux launcher
# Usage: bash START_HAMED_ANDROID.sh

cd "$(dirname "$0")" || exit 1

echo "========================================"
echo "       HAMED AI - ANDROID START"
echo "========================================"
echo

if ! command -v python >/dev/null 2>&1; then
  echo "ERROR: Python is not installed in Termux."
  echo "Run: pkg update && pkg install python"
  exit 1
fi

if [ ! -f "app/main.py" ]; then
  echo "ERROR: app/main.py was not found."
  echo "Make sure this script is inside the Hamed project folder."
  exit 1
fi

if command -v termux-wake-lock >/dev/null 2>&1; then
  termux-wake-lock
fi

python -m app.main
