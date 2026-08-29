"""Outbound phone-call controller for Hamed.

This module creates calls through Twilio. Credentials are read from environment
variables and are never stored in source control.
"""
import os
from dataclasses import dataclass
from twilio.rest import Client


@dataclass(frozen=True)
class CallRequest:
    to: str
    session_id: str
    base_url: str


class VoiceCallController:
    def __init__(self) -> None:
        self.account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        self.auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.from_number = os.environ.get("TWILIO_FROM_NUMBER")
        if not all((self.account_sid, self.auth_token, self.from_number)):
            raise RuntimeError("TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER are required")
        self.client = Client(self.account_sid, self.auth_token)

    def start_call(self, request: CallRequest) -> str:
        """Start an outbound call; the public HTTPS URL supplies TwiML."""
        webhook = request.base_url.rstrip("/") + f"/voice/twiml/{request.session_id}"
        call = self.client.calls.create(
            to=request.to,
            from_=self.from_number,
            url=webhook,
            method="POST",
        )
        return call.sid
