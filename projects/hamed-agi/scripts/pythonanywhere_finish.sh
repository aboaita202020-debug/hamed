#!/usr/bin/env bash
set -euo pipefail

cd "$HOME/hamed-agi"

echo "[1/6] Syncing HAMED AGI"
git fetch origin main
git reset --hard origin/main

echo "[2/6] Installing dependencies"
source "$HOME/.virtualenvs/hamed_venv/bin/activate"
python -m pip install -r requirements.txt

echo "[3/6] Creating server-side control secret if missing"
mkdir -p data
if [ ! -s data/control_secret ]; then
  python - <<'PY'
import secrets
from pathlib import Path
p = Path("data/control_secret")
p.write_text(secrets.token_urlsafe(32) + "\n", encoding="utf-8")
p.chmod(0o600)
print("control secret created")
PY
else
  echo "control secret already present"
fi

echo "[4/6] Running tests"
python -m pytest -q

echo "[5/6] Reloading PythonAnywhere website"
python -m pip install --upgrade pythonanywhere
pa website reload --domain aboaita2011.pythonanywhere.com

echo "[6/6] Verifying public endpoints"
sleep 3
curl -fsS https://aboaita2011.pythonanywhere.com/health
curl -fsS https://aboaita2011.pythonanywhere.com/readiness
curl -fsS https://aboaita2011.pythonanywhere.com/status
curl -fsS -o /dev/null -w "dashboard HTTP %{http_code}\n" https://aboaita2011.pythonanywhere.com/dashboard
echo "DEPLOYMENT_OK"
