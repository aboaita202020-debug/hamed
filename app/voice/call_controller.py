"""Outbound phone-call controller for Hamed.

Credentials stay in environment variables. Targets must be explicitly allowlisted
before a call is placed.
"""
import os
from dataclasses import dataclass
from twilio.rest import Client
from .voice_policy import CallPolicy, validate_attempt_count, validate_outbound_target


@dataclass(frozen=True)
class CallRequest:
    to: str
    session_id: str
    base_url: str
    attempts: int = 0
    allowlist: frozenset[str] = frozenset()


class VoiceCallController:
    def __init__(self, policy: CallPolicy | None = None) -> None:
        self.account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        self.auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.from_number = os.environ.get("TWILIO_FROM_NUMBER")
        if not all((self.account_sid, self.auth_token, self.from_number)):
            raise RuntimeError("TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER are required")
        self.policy = policy or CallPolicy()
        self.client = Client(self.account_sid, self.auth_token)

    def start_call(self, request: CallRequest) -> str:
        validate_outbound_target(request.to, set(request.allowlist))
        validate_attempt_count(request.attempts, self.policy)
        webhook = request.base_url.rstrip("/") + f"/voice/twiml/{request.session_id}"
        call = self.client.calls.create(
            to=request.to,
            from_=self.from_number,
            url=webhook,
            method="POST",
        )
        return call.sid
