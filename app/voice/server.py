"""FastAPI bridge: Twilio Media Streams <-> OpenAI Realtime for Hamed."""
import asyncio
import json
import os
from typing import Any

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from websockets.asyncio.client import connect

from .sales_context import SalesContext

app = FastAPI(title="Hamed Voice Sales Agent")

VOICE_SYSTEM_PROMPT = os.environ.get(
    "HAMED_VOICE_SYSTEM_PROMPT",
    """You are Hamed AI, a professional commercial sales assistant.
Identify yourself as an AI assistant at the beginning of an outbound call and state the business purpose.
Be warm, concise, consultative and honest. Discover the customer's needs before proposing an offer.
Use the PRE-CALL SALES BRIEF as context, but treat only verified fields as facts and never invent missing information.
For website, e-commerce, marketing, affiliate and other services, diagnose the customer's real need and propose only relevant services.
Use value-based selling, active listening and ethical negotiation. Never pressure, deceive, impersonate a human, or guarantee outcomes.
Respect a clear request to end the call and do not repeatedly contact a person who declines.
For purchases, payments, contracts, discounts below the configured floor, or other high-impact actions, require human approval.
The goal is a mutually beneficial agreement, customer satisfaction and long-term commercial value.""",
)

# Demo-safe in-memory registry. Production should replace this with the project's CRM/session store.
SALES_CONTEXTS: dict[str, SalesContext] = {}


def twiml_for_session(session_id: str, public_base_url: str) -> str:
    ws_url = public_base_url.replace("https://", "wss://").replace("http://", "ws://").rstrip("/")
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <Stream url="{ws_url}/voice/stream/{session_id}" />
  </Connect>
</Response>'''


@app.post("/voice/twiml/{session_id}")
async def voice_twiml(session_id: str, request: Request) -> Response:
    public_base_url = os.environ.get("PUBLIC_BASE_URL") or str(request.base_url).rstrip("/")
    return Response(twiml_for_session(session_id, public_base_url), media_type="application/xml")


def register_sales_context(session_id: str, context: SalesContext) -> None:
    SALES_CONTEXTS[session_id] = context


async def _send_openai_session_config(openai_ws: Any, session_id: str) -> None:
    context = SALES_CONTEXTS.get(session_id, SalesContext())
    instructions = VOICE_SYSTEM_PROMPT + "\n\n" + context.as_prompt()
    await openai_ws.send(json.dumps({
        "type": "session.update",
        "session": {
            "type": "realtime",
            "model": os.environ.get("OPENAI_REALTIME_MODEL", "gpt-realtime-2.1-mini"),
            "output_modalities": ["audio"],
            "instructions": instructions,
            "audio": {
                "input": {"format": {"type": "audio/pcmu"}},
                "output": {"format": {"type": "audio/pcmu"}},
            },
        },
    }))


async def _start_greeting(openai_ws: Any) -> None:
    greeting = (
        "ابدأ بتحية قصيرة باللهجة المصرية، واذكر بوضوح أنك مساعد ذكاء اصطناعي "
        "تتصل لمناقشة فرصة تجارية حقيقية، ثم اسأل هل الوقت مناسب لدقيقة. "
        "لا تبدأ بعرض سعر؛ ابدأ باكتشاف الاحتياج."
    )
    await openai_ws.send(json.dumps({
        "type": "conversation.item.create",
        "item": {
            "type": "message",
            "role": "user",
            "content": [{"type": "input_text", "text": greeting}],
        },
    }))
    await openai_ws.send(json.dumps({"type": "response.create"}))


@app.websocket("/voice/stream/{session_id}")
async def voice_stream(websocket: WebSocket, session_id: str) -> None:
    await websocket.accept()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        await websocket.close(code=1011, reason="OPENAI_API_KEY is not configured")
        return

    realtime_url = os.environ.get(
        "OPENAI_REALTIME_URL",
        "wss://api.openai.com/v1/realtime?model=gpt-realtime-2.1-mini",
    )
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        async with connect(realtime_url, additional_headers=headers, max_size=None) as openai_ws:
            await _send_openai_session_config(openai_ws, session_id)
            await _start_greeting(openai_ws)
            stream_sid: str | None = None

            async def twilio_to_openai() -> None:
                nonlocal stream_sid
                while True:
                    raw = await websocket.receive_text()
                    event = json.loads(raw)
                    kind = event.get("event")
                    if kind == "start":
                        stream_sid = event["start"]["streamSid"]
                    elif kind == "media":
                        await openai_ws.send(json.dumps({
                            "type": "input_audio_buffer.append",
                            "audio": event["media"]["payload"],
                        }))
                    elif kind == "stop":
                        break

            async def openai_to_twilio() -> None:
                async for raw in openai_ws:
                    event = json.loads(raw)
                    event_type = event.get("type")
                    if event_type in {"response.output_audio.delta", "response.audio.delta"} and stream_sid:
                        payload = event.get("delta") or event.get("audio")
                        if payload:
                            await websocket.send_text(json.dumps({
                                "event": "media",
                                "streamSid": stream_sid,
                                "media": {"payload": payload},
                            }))
                    elif event_type == "error":
                        break

            await asyncio.gather(twilio_to_openai(), openai_to_twilio())
    except WebSocketDisconnect:
        return
    except Exception:
        try:
            await websocket.close(code=1011, reason="voice bridge stopped")
        except Exception:
            pass
