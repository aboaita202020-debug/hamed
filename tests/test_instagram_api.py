from __future__ import annotations

from app.channels.instagram import InstagramAdapter


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def test_instagram_status_uses_account_endpoint(monkeypatch):
    calls = []

    def fake_request(method, url, **kwargs):
        calls.append((method, url, kwargs))
        return FakeResponse({"user_id": "123", "username": "mlovenoor"})

    monkeypatch.setattr("app.channels.instagram.requests.request", fake_request)
    result = InstagramAdapter(access_token="secret").status()
    assert result["authenticated"] is True
    assert result["username"] == "mlovenoor"
    assert calls[0][0] == "GET"
    assert "graph.instagram.com" in calls[0][1]
    assert calls[0][2]["params"]["access_token"] == "secret"


def test_send_message_posts_expected_payload(monkeypatch):
    calls = []

    def fake_request(method, url, **kwargs):
        calls.append((method, url, kwargs))
        if method == "GET":
            return FakeResponse({"user_id": "123", "username": "mlovenoor"})
        return FakeResponse({"recipient_id": "456", "message_id": "m1"})

    monkeypatch.setattr("app.channels.instagram.requests.request", fake_request)
    result = InstagramAdapter(access_token="secret").send_message("456", "Hello")
    assert result["message_id"] == "m1"
    assert calls[-1][0] == "POST"
    assert calls[-1][2]["json"]["recipient"]["id"] == "456"
    assert calls[-1][2]["json"]["message"]["text"] == "Hello"


def test_create_reel_container_posts_public_video_url(monkeypatch):
    calls = []

    def fake_request(method, url, **kwargs):
        calls.append((method, url, kwargs))
        if method == "GET":
            return FakeResponse({"user_id": "123", "username": "mlovenoor"})
        return FakeResponse({"id": "container-1"})

    monkeypatch.setattr("app.channels.instagram.requests.request", fake_request)
    result = InstagramAdapter(access_token="secret").create_reel_container(
        "https://example.com/video.mp4",
        "Hamed AGI",
    )
    assert result["id"] == "container-1"
    assert calls[-1][0] == "POST"
    assert calls[-1][2]["params"]["media_type"] == "REELS"
    assert calls[-1][2]["params"]["video_url"].startswith("https://")


def test_publish_reel_waits_for_finished_container(monkeypatch):
    calls = []

    def fake_request(method, url, **kwargs):
        calls.append((method, url, kwargs))
        if method == "GET" and url.endswith("/me"):
            return FakeResponse({"user_id": "123", "username": "mlovenoor"})
        if method == "POST" and url.endswith("/123/media"):
            return FakeResponse({"id": "container-1"})
        if method == "GET" and url.endswith("/container-1"):
            return FakeResponse({"status_code": "FINISHED", "status": "Finished"})
        if method == "POST" and url.endswith("/123/media_publish"):
            return FakeResponse({"id": "published-1"})
        raise AssertionError((method, url))

    monkeypatch.setattr("app.channels.instagram.requests.request", fake_request)
    result = InstagramAdapter(access_token="secret").publish_reel(
        "https://example.com/video.mp4",
        "Hamed AGI",
        wait_seconds=2,
        poll_seconds=0.2,
    )
    assert result["status"] == "ready_and_published"
    assert result["published"]["id"] == "published-1"
