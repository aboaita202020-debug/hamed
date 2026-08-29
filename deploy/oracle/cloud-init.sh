#!/bin/bash
set -euo pipefail

# Hamed AI - Oracle Cloud Always Free bootstrap
# Run as root on a fresh Ubuntu VM. Secrets are intentionally NOT stored here.

apt-get update
apt-get install -y python3 python3-venv python3-pip git

APP_DIR=/opt/hamed
REPO_URL=https://github.com/aboaita202020-debug/hamed.git

if [ ! -d "$APP_DIR/.git" ]; then
  git clone "$REPO_URL" "$APP_DIR"
else
  git -C "$APP_DIR" pull --ff-only
fi

python3 -m venv "$APP_DIR/.venv"
"$APP_DIR/.venv/bin/pip" install --upgrade pip
"$APP_DIR/.venv/bin/pip" install -r "$APP_DIR/requirements.txt"

mkdir -p /etc/hamed "$APP_DIR/data"
chmod 700 /etc/hamed

cat >/etc/systemd/system/hamed.service <<'UNIT'
[Unit]
Description=Hamed AI Commercial Agent
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/opt/hamed
EnvironmentFile=-/etc/hamed/hamed.env
Environment=HAMED_HOST=0.0.0.0
Environment=HAMED_PORT=8000
ExecStart=/opt/hamed/.venv/bin/python /opt/hamed/cloud_server.py
Restart=always
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/hamed/data

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable hamed.service
systemctl restart hamed.service

echo 'Hamed installed. Put real secrets in /etc/hamed/hamed.env, then: systemctl restart hamed'
