"""Instagram webhook receiver with verification, signature checks, and CRM handoff."""
from __future__ import annotations

import hashlib
import hmac
import json
import os
from typing import Any

from fastapi import APIRouter, HTTPException, Request

from .db.database import get_database
from .db.repository import Repository

router = APIRouter(prefix="/webhooks/instagram", tags=["instagram-webhooks"])


def _verify_token() -> str:
    return os.getenv("INSTAGRAM_WEBHOOK_VERIFY_TOKEN", "")


def _app_secret() -> str:
    return os.getenv("META_APP_SECRET", "")


def _signature_valid(raw_body: bytes, header: str | None) -> bool:
    secret = _app_secret()
    if not secret:
        return False
    if not header or not header.startswith("sha256="):
        return False
    expected = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(header[7:], expected)


def _text_from_item(item: dict[str, Any]) -> str:
    message = item.get("message")
    if isinstance(message, dict) and isinstance(message.get("text"), str):
        return message["text"]
    changes = item.get("changes")
    if isinstance(changes, list):
        for change in changes:
            value = change.get("value", {}) if isinstance(change, dict) else {}
            if isinstance(value, dict):
                text = value.get("text")
                if isinstance(text, str):
                    return text
                comment = value.get("text")
                if isinstance(comment, str):
                    return comment
    return ""


def extract_interactions(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Normalize common messaging/comment webhook shapes into CRM-ready events."""
    interactions: list[dict[str, Any]] = []
    for entry in payload.get("entry", []) if isinstance(payload.get("entry"), list) else []:
        if not isinstance(entry, dict):
            continue
        for item in entry.get("messaging", []) if isinstance(entry.get("messaging"), list) else []:
            if not isinstance(item, dict):
                continue
            sender = item.get("sender", {})
            sender_id = sender.get("id") if isinstance(sender, dict) else None
            text = _text_from_item(item)
            if sender_id:
                interactions.append({"type": "message", "sender_id": str(sender_id), "text": text, "raw": item})
        for change in entry.get("changes", []) if isinstance(entry.get("changes"), list) else []:
            if not isinstance(change, dict):
                continue
            value = change.get("value", {})
            if not isinstance(value, dict):
                continue
            from_data = value.get("from", {})
            sender_id = from_data.get("id") if isinstance(from_data, dict) else None
            if sender_id:
                interactions.append({"type": change.get("field", "change"), "sender_id": str(sender_id), "text": value.get("text", ""), "raw": change})
    return interactions


def persist_interactions(interactions: list[dict[str, Any]]) -> int:
    repo = Repository(get_database())
    count = 0
    for event in interactions:
        sender_id = event.get("sender_id")
        if not sender_id:
            continue
        repo.upsert_lead(
            name=f"Instagram {sender_id}",
            contact=f"instagram:{sender_id}",
            source="instagram_webhook",
            activity=event.get("type", "interaction"),
            interest=event.get("text", ""),
            stage="INBOUND_CONTACT",
            notes=json.dumps(event.get("raw", {}), ensure_ascii=False, default=str),
        )
        count += 1
    return count


@router.get("")
async def verify_webhook(request: Request) -> Any:
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")
    expected = _verify_token()
    if mode == "subscribe" and expected and hmac.compare_digest(token or "", expected) and challenge:
        return int(challenge) if challenge.isdigit() else challenge
    raise HTTPException(status_code=403, detail="Webhook verification failed")


@router.post("")
async def receive_webhook(request: Request) -> dict[str, Any]:
    raw_body = await request.body()
    signature = request.headers.get("x-hub-signature-256")
    if not _signature_valid(raw_body, signature):
        raise HTTPException(status_code=403, detail="Invalid webhook signature")
    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=400, detail="Invalid JSON payload") from exc
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Webhook payload must be an object")
    interactions = extract_interactions(payload)
    persisted = persist_interactions(interactions)
    return {"status": "received", "interactions": len(interactions), "persisted": persisted, "auto_reply": False}
