#!/data/data/com.termux/files/usr/bin/bash

# Hamed AI - one-tap Termux:Widget shortcut
# Place this file in: ~/.shortcuts/HAMED_AI.sh

PROJECT_DIR="${HOME}/hamed"
if [ ! -d "$PROJECT_DIR" ]; then
  PROJECT_DIR="${HOME}/hamed-ai"
fi

if [ ! -d "$PROJECT_DIR" ]; then
  echo "Hamed project folder not found. Expected: $HOME/hamed"
  exit 1
fi

cd "$PROJECT_DIR" || exit 1

if command -v termux-wake-lock >/dev/null 2>&1; then
  termux-wake-lock
fi

if [ ! -f "app/main.py" ]; then
  echo "app/main.py not found in $PROJECT_DIR"
  exit 1
fi

python -m app.main
