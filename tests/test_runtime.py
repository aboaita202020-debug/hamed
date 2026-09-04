import pytest

from app.runtime import http_host, http_port


def test_hamed_listener_settings_override_platform_defaults(monkeypatch):
    monkeypatch.setenv("HAMED_HOST", "127.0.0.1")
    monkeypatch.setenv("HAMED_PORT", "9010")
    monkeypatch.setenv("PORT", "8000")

    assert http_host() == "127.0.0.1"
    assert http_port() == 9010


def test_listener_settings_fall_back_to_platform_port(monkeypatch):
    monkeypatch.delenv("HAMED_HOST", raising=False)
    monkeypatch.delenv("HAMED_PORT", raising=False)
    monkeypatch.setenv("PORT", "8123")

    assert http_host() == "0.0.0.0"
    assert http_port() == 8123


@pytest.mark.parametrize("value", ("not-a-port", "0", "65536"))
def test_listener_port_rejects_invalid_values(monkeypatch, value):
    monkeypatch.setenv("HAMED_PORT", value)

    with pytest.raises(ValueError, match="HAMED_PORT or PORT"):
        http_port()
