from __future__ import annotations

import hashlib
import hmac
import json

from fastapi.testclient import TestClient


def test_webhook_verification(monkeypatch):
    monkeypatch.setenv("INSTAGRAM_WEBHOOK_VERIFY_TOKEN", "verify-me")
    from app.main import app
    client = TestClient(app)
    response = client.get("/webhooks/instagram", params={"hub.mode": "subscribe", "hub.verify_token": "verify-me", "hub.challenge": "12345"})
    assert response.status_code == 200
    assert response.text == "12345"


def test_webhook_rejects_invalid_signature(monkeypatch):
    monkeypatch.setenv("META_APP_SECRET", "secret")
    from app.main import app
    client = TestClient(app)
    response = client.post("/webhooks/instagram", content=b"{}", headers={"x-hub-signature-256": "sha256=bad"})
    assert response.status_code == 403


def test_webhook_persists_inbound_interaction(monkeypatch):
    secret = "secret"
    monkeypatch.setenv("META_APP_SECRET", secret)
    from app import instagram_webhooks
    monkeypatch.setattr(instagram_webhooks, "persist_interactions", lambda events: len(events))
    payload = {"entry": [{"messaging": [{"sender": {"id": "456"}, "message": {"text": "Hello Hamed"}}]}]}
    raw = json.dumps(payload).encode()
    signature = hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()
    from app.main import app
    client = TestClient(app)
    response = client.post("/webhooks/instagram", content=raw, headers={"x-hub-signature-256": f"sha256={signature}"})
    assert response.status_code == 200
    assert response.json()["interactions"] == 1
    assert response.json()["persisted"] == 1
