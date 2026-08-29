# Hamed Voice Sales Agent

Hamed can place outbound calls through Twilio and stream the live call audio to OpenAI Realtime.

## Required environment

```text
OPENAI_API_KEY=...
OPENAI_REALTIME_MODEL=gpt-realtime-2.1-mini
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_FROM_NUMBER=...
PUBLIC_BASE_URL=https://your-public-https-host
```

## Run

```bash
uvicorn app.voice.server:app --host 0.0.0.0 --port 8000
```

The public host must support HTTPS and WSS so Twilio can reach `/voice/twiml/{session_id}` and `/voice/stream/{session_id}`.

## Start an outbound call

Use `VoiceCallController`:

```python
from app.voice.call_controller import CallRequest, VoiceCallController

controller = VoiceCallController()
call_sid = controller.start_call(
    CallRequest(to="+201XXXXXXXXX", session_id="customer-123", base_url="https://your-host.example")
)
print(call_sid)
```

## Safety

- Keep Twilio and OpenAI secrets in environment variables or a secret manager.
- Identify Hamed as an AI assistant where required.
- Respect applicable calling, privacy, consent and anti-spam rules.
- Keep purchases, payments, contracts and other high-impact actions behind Hamed's existing approval gate.
- Start with verified/test numbers before production outreach.
