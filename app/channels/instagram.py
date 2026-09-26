"""Instagram API with Instagram Login adapter."""
from __future__ import annotations

import os
import time
from typing import Any

import requests


class InstagramAdapter:
    def __init__(
        self,
        access_token: str | None = None,
        api_version: str | None = None,
        timeout: float = 20.0,
    ) -> None:
        self.access_token = access_token or os.getenv("INSTAGRAM_ACCESS_TOKEN")
        self.api_version = api_version or os.getenv("INSTAGRAM_API_VERSION", "v24.0")
        self.timeout = timeout
        self.base_url = f"https://graph.instagram.com/{self.api_version}"

    @property
    def configured(self) -> bool:
        return bool(self.access_token)

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        if not self.access_token:
            raise RuntimeError("Instagram access token is not configured")
        params = dict(kwargs.pop("params", {}))
        params["access_token"] = self.access_token
        response = requests.request(
            method,
            f"{self.base_url}/{path.lstrip('/')}",
            params=params,
            timeout=self.timeout,
            **kwargs,
        )
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise RuntimeError("Instagram API returned an unexpected response")
        return data

    def account(self) -> dict[str, Any]:
        return self._request("GET", "me", params={"fields": "user_id,username"})

    def status(self) -> dict[str, Any]:
        if not self.configured:
            return {
                "configured": False,
                "authenticated": False,
                "reason": "INSTAGRAM_ACCESS_TOKEN is not configured",
            }
        try:
            data = self.account()
            return {
                "configured": True,
                "authenticated": True,
                "username": data.get("username"),
                "user_id": data.get("user_id"),
            }
        except requests.RequestException as exc:
            return {"configured": True, "authenticated": False, "error": str(exc)}

    def create_reel_container(
        self,
        video_url: str,
        caption: str = "",
        share_to_feed: bool = True,
    ) -> dict[str, Any]:
        """Create a Reel container from a publicly reachable video URL."""
        account = self.account()
        return self._request(
            "POST",
            f"{account['user_id']}/media",
            params={
                "media_type": "REELS",
                "video_url": video_url,
                "caption": caption,
                "share_to_feed": str(bool(share_to_feed)).lower(),
            },
        )

    def container_status(self, container_id: str) -> dict[str, Any]:
        return self._request(
            "GET",
            container_id,
            params={"fields": "status_code,status"},
        )

    def publish_container(self, container_id: str) -> dict[str, Any]:
        account = self.account()
        return self._request(
            "POST",
            f"{account['user_id']}/media_publish",
            params={"creation_id": container_id},
        )

    def publish_reel(
        self,
        video_url: str,
        caption: str = "",
        share_to_feed: bool = True,
        wait_seconds: int = 120,
        poll_seconds: float = 3.0,
    ) -> dict[str, Any]:
        """Create, wait for readiness, and publish a Reel."""
        container = self.create_reel_container(video_url, caption, share_to_feed)
        container_id = container.get("id")
        if not container_id:
            raise RuntimeError("Instagram did not return a media container id")

        deadline = time.monotonic() + max(1, wait_seconds)
        last_status: dict[str, Any] = {}
        while time.monotonic() < deadline:
            last_status = self.container_status(container_id)
            code = str(last_status.get("status_code", "")).upper()
            if code == "FINISHED":
                return {
                    "status": "ready_and_published",
                    "container_id": container_id,
                    "container_status": last_status,
                    "published": self.publish_container(container_id),
                }
            if code in {"ERROR", "EXPIRED"}:
                raise RuntimeError(
                    f"Instagram media container failed: {last_status.get('status') or code}"
                )
            time.sleep(max(0.2, poll_seconds))

        raise TimeoutError(
            f"Instagram media container did not become ready in {wait_seconds}s: {last_status}"
        )

    def send_message(self, recipient_id: str, text: str) -> dict[str, Any]:
        """Send a text DM to an Instagram-scoped recipient."""
        if not recipient_id.strip():
            raise ValueError("recipient_id is required")
        if not text.strip():
            raise ValueError("message text is required")
        account = self.account()
        return self._request(
            "POST",
            f"{account['user_id']}/messages",
            json={
                "recipient": {"id": recipient_id},
                "message": {"text": text},
            },
        )


def instagram_status() -> dict[str, Any]:
    return InstagramAdapter().status()
