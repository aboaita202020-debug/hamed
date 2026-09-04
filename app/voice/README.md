# Hamed Voice Sales Agent

Hamed can place outbound calls through Twilio and stream the live call audio to OpenAI Realtime.

## Hamed work number

The configured Hamed work caller ID is **+20104090623**. Set `TWILIO_FROM_NUMBER=+20104090623` explicitly in the deployment environment; the code also uses this number as its safe default when the variable is omitted.

The number must be owned/verified and enabled for outbound calling by the Twilio account. Code changes cannot provision or verify the number with Twilio.

## Required environment

```text
OPENAI_API_KEY=...
OPENAI_REALTIME_MODEL=gpt-realtime-2.1-mini
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_FROM_NUMBER=+20104090623
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

The controller sends the call with `from_` set to Hamed's configured work number. Targets must still pass the existing allowlist and attempt policy.

## Safety

- Keep Twilio and OpenAI secrets in environment variables or a secret manager.
- Identify Hamed as an AI assistant where required.
- Respect applicable calling, privacy, consent and anti-spam rules.
- Keep purchases, payments, contracts and other high-impact actions behind Hamed's existing approval gate.
- Start with verified/test numbers before production outreach.
