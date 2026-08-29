"""FastAPI bridge: Twilio Media Streams <-> OpenAI Realtime for Hamed.

Credentials remain server-side. The bridge is intentionally approval-aware:
voice calls can qualify and sell services, but it must not make high-impact
commitments on behalf of the owner.
"""
import asyncio
import json
import os
from typing import Any

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from websockets.asyncio.client import connect

app = FastAPI(title="Hamed Voice Sales Agent")

VOICE_SYSTEM_PROMPT = os.environ.get(
    "HAMED_VOICE_SYSTEM_PROMPT",
    """You are Hamed AI, a professional commercial sales assistant.
At the beginning of an outbound call, clearly identify yourself as an AI assistant and state the business purpose of the call.
Be warm, concise, consultative and honest. Discover the customer's needs before proposing an offer.
For website, e-commerce, marketing, affiliate and other services, diagnose the customer's real need and propose only relevant services.
Never invent facts about the customer's business, website, prices, results or capabilities.
Never pressure, deceive, impersonate a human, or guarantee outcomes.
Respect a clear request to end the call and do not repeatedly contact a person who declines.
Do not request or expose sensitive personal data unnecessarily.
For purchases, payments, contracts, discounts below the configured floor, or other high-impact actions, require human approval.
Your goal is a mutually beneficial agreement, customer satisfaction and long-term commercial value.""",
)


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


async def _send_openai_session_config(openai_ws: Any) -> None:
    await openai_ws.send(json.dumps({
        "type": "session.update",
        "session": {
            "type": "realtime",
            "model": os.environ.get("OPENAI_REALTIME_MODEL", "gpt-realtime-2.1-mini"),
            "output_modalities": ["audio"],
            "instructions": VOICE_SYSTEM_PROMPT,
            "audio": {
                "input": {"format": {"type": "audio/pcmu"}},
                "output": {"format": {"type": "audio/pcmu"}},
            },
        },
    }))


async def _start_greeting(openai_ws: Any) -> None:
    greeting = (
        "ابدأ المكالمة بتحية قصيرة باللغة العربية المصرية، واذكر بوضوح أنك مساعد ذكاء اصطناعي "
        "تتصل من أجل مناقشة فرصة لتحسين النشاط التجاري، ثم اسأل هل الوقت مناسب لدقيقة."
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
            await _send_openai_session_config(openai_ws)
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
