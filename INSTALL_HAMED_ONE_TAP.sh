#!/data/data/com.termux/files/usr/bin/bash

# Hamed AI - install one-tap Android shortcut for Termux:Widget
set -e

cd "$(dirname "$0")" || exit 1
mkdir -p "$HOME/.shortcuts"

if [ ! -f ".shortcuts/HAMED_AI.sh" ]; then
  echo "ERROR: .shortcuts/HAMED_AI.sh is missing from the Hamed project."
  exit 1
fi

cp ".shortcuts/HAMED_AI.sh" "$HOME/.shortcuts/HAMED_AI.sh"
chmod +x "$HOME/.shortcuts/HAMED_AI.sh"

echo "========================================"
echo " Hamed AI - ONE TAP READY"
echo "========================================"
echo

echo "The shortcut is installed in Termux:Widget."
echo "Add the Hamed AI shortcut/widget to the Android home screen."
echo "After that, one tap starts Hamed."
echo
