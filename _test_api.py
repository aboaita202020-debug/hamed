"""Smoke test for FastAPI endpoints — runs without network calls except LLM."""
from __future__ import annotations
import sys
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["name"] == "Hamed AI"

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "ai_provider" in data
    assert data["telegram"] is False

def test_chat():
    r = client.post("/chat", json={"session_id": "smoke", "message": "hello"})
    assert r.status_code == 200
    assert "reply" in r.json()
    print("CHAT:", r.json()["reply"][:80])

def test_plan():
    r = client.post("/plan", json={"message": "find new clients", "action": "research"})
    assert r.status_code == 200
    data = r.json()
    assert "objective" in data
    assert "next_steps" in data
    print("PLAN:", data["objective"])

def test_offer():
    r = client.post("/offer", json={"company": "Salla", "product": "e-commerce"})
    assert r.status_code == 200
    offer = r.json()["offer"]
    assert len(offer) > 50
    print("OFFER:", offer[:200])

def test_worker_run():
    r = client.post("/worker/run")
    assert r.status_code == 200
    print("WORKER:", r.json()["status"])

if __name__ == "__main__":
    test_root()
    test_health()
    test_chat()
    test_plan()
    test_offer()
    test_worker_run()
    print("\nALL API TESTS PASSED")
