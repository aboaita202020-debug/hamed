"""Provider-neutral WhatsApp channel contract."""
from dataclasses import dataclass

@dataclass(frozen=True)
class IncomingMessage:
    sender_id: str
    text: str
    message_id: str

class WhatsAppAdapter:
    def parse_message(self, payload: dict) -> IncomingMessage:
        raise NotImplementedError

    def send_message(self, recipient: str, text: str) -> str:
        raise NotImplementedError
