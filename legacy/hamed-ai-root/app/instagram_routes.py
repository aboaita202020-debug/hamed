from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from .channels.instagram import InstagramAdapter, instagram_status


router = APIRouter(prefix="/instagram", tags=["instagram"])


class InstagramReelRequest(BaseModel):
    video_url: str = Field(min_length=10, max_length=4000)
    caption: str = Field(default="", max_length=2200)
    share_to_feed: bool = True
    approved: bool = False


class InstagramMessageRequest(BaseModel):
    recipient_id: str = Field(min_length=3, max_length=200)
    message: str = Field(min_length=1, max_length=4000)
    permitted_contact: bool = False


@router.get("/status")
def status() -> dict[str, Any]:
    return instagram_status()


@router.post("/publish/reel")
def publish_reel(request: InstagramReelRequest) -> dict[str, Any]:
    if not request.approved:
        raise HTTPException(
            status_code=403,
            detail="Publishing requires explicit approval.",
        )
    try:
        result = InstagramAdapter().publish_reel(
            request.video_url,
            request.caption,
            request.share_to_feed,
        )
        return {"status": "ok", **result}
    except (RuntimeError, TimeoutError, ValueError) as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/messages/send")
def send_message(request: InstagramMessageRequest) -> dict[str, Any]:
    if not request.permitted_contact:
        raise HTTPException(
            status_code=403,
            detail="A permitted Instagram contact is required.",
        )
    try:
        result = InstagramAdapter().send_message(
            request.recipient_id,
            request.message,
        )
        return {"status": "sent", **result}
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
