"""Google OAuth 2.0 integration for Hamed.

Uses delegated authorization; passwords are never accepted or stored. Configure
client ID/secret and redirect URI through deployment secrets.
"""
from __future__ import annotations

import os
import secrets
from typing import Any

from google_auth_oauthlib.flow import Flow

SCOPES = tuple(filter(None, os.getenv("GOOGLE_OAUTH_SCOPES", "openid,email,https://www.googleapis.com/auth/gmail.readonly").split(",")))


def _flow(state: str | None = None) -> Flow:
    client_config = {
        "web": {
            "client_id": os.environ["GOOGLE_CLIENT_ID"],
            "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
            "auth_uri": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [os.environ["GOOGLE_REDIRECT_URI"]],
        }
    }
    flow = Flow.from_client_config(client_config, scopes=list(SCOPES), state=state)
    flow.redirect_uri = os.environ["GOOGLE_REDIRECT_URI"]
    return flow


def authorization_url() -> tuple[str, str]:
    state = secrets.token_urlsafe(32)
    url, returned_state = _flow(state).authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
        login_hint=os.getenv("GOOGLE_ADMIN_EMAIL", ""),
    )
    return url, returned_state


def exchange_code(code: str, state: str) -> dict[str, Any]:
    flow = _flow(state)
    flow.fetch_token(code=code)
    credentials = flow.credentials
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "expiry": credentials.expiry.isoformat() if credentials.expiry else None,
        "scopes": list(credentials.scopes or SCOPES),
    }
