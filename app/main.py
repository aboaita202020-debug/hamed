"""Unified Hamed AI application entrypoint."""
from __future__ import annotations

import html
import os
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from .agents.commercial_brain import build_plan
from .agents.orchestrator import HamedOrchestrator
from .agents.provider import OpenAIProvider
from .config import settings


class FallbackProvider:
    """No-cost deterministic provider used when no OpenAI key is configured."""

    def generate_response(self, messages: list[dict[str, str]], *, system: str = "") -> str:
        text = messages[-1].get("content", "") if messages else ""
        lower = text.lower()
        if any(k in lower for k in ("شراء", "اشتري", "مشتريات", "شراء منتج")):
            return "أقدر أساعدك في تقييم الشراء وحساب التكلفة والربح والمخاطر، لكن تنفيذ الشراء نفسه يحتاج موافقة صريحة."
        if any(k in lower for k in ("موقع", "متجر", "website", "store")):
            return "أقدر أراجع احتياج النشاط، أحدد المشاكل أو المتطلبات، وأجهز عرض موقع أو متجر مناسب بناءً على معلومات مؤكدة."
        if any(k in lower for k in ("تسويق بالعمولة", "affiliate", "عمولة")):
            return "أقدر أقيّم برامج التسويق بالعمولة حسب جودة المنتج، ملاءمة الجمهور، العمولة، التحويلات والمخاطر، ثم أبني خطة اختبار."
        if any(k in lower for k in ("تفاوض", "السعر", "خصم")):
            return "أقدر أبني استراتيجية تفاوض تحافظ على القيمة وتستخدم حدود السعر والخصم المسموح بها بدون اختلاق عروض أو معلومات."
        return "أنا حامد. اكتب هدفك التجاري، وسأحوّله إلى بحث وتحليل وخطوات تنفيذ مناسبة."

    def web_research(self, query: str, *, system: str = "") -> str:
        return "وضع التشغيل المجاني لا يحتوي على مزود بحث خارجي مفعّل. أضف OPENAI_API_KEY لتفعيل البحث المباشر عبر مزود الذكاء الاصطناعي."


class ChatRequest(BaseModel):
    session_id: str = Field(default="default", min_length=1, max_length=120)
    message: str = Field(min_length=1, max_length=12000)


class PlanRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    action: str | None = Field(default=None, max_length=80)


class ActionRequest(BaseModel):
    session_id: str = Field(default="default", min_length=1, max_length=120)
    action: str = Field(min_length=1, max_length=80)
    description: str = Field(min_length=1, max_length=2000)
    value: float | None = None


class DecisionRequest(BaseModel):
    session_id: str = Field(default="default", min_length=1, max_length=120)
    action: str = Field(min_length=1, max_length=80)
    approved: bool


app = FastAPI(title="Hamed AI", version="0.3.0", docs_url="/docs")
_provider = OpenAIProvider(settings.openai_api_key, settings.openai_model) if settings.openai_api_key else FallbackProvider()
_orchestrator = HamedOrchestrator(_provider)
_pending: dict[tuple[str, str], Any] = {}


@app.get("/")
def root() -> dict[str, str]:
    return {"name": "Hamed AI", "status": "running", "mode": settings.app_env}


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "ai_provider": "openai" if settings.openai_api_key else "fallback",
        "telegram": bool(settings.telegram_bot_token),
        "voice": bool(os.getenv("TWILIO_ACCOUNT_SID") and os.getenv("TWILIO_AUTH_TOKEN")),
        "autonomous_mode": settings.autonomous_mode,
    }


@app.post("/chat")
def chat(request: ChatRequest) -> dict[str, str]:
    try:
        reply = _orchestrator.respond(request.session_id, request.message)
        return {"session_id": request.session_id, "reply": reply}
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/plan")
def plan(request: PlanRequest) -> dict[str, Any]:
    result = build_plan(request.message, action=request.action)
    return {
        "objective": result.objective.value,
        "intent": result.intent,
        "next_steps": result.next_steps,
        "requires_research": result.requires_research,
        "approval_required": result.approval_required,
        "confidence": result.confidence,
        "notes": result.notes,
    }


@app.post("/actions/prepare")
def prepare(request: ActionRequest) -> dict[str, Any]:
    message = _orchestrator.prepare_high_impact_action(
        request.session_id,
        request.action,
        request.description,
        request.value,
    )
    _pending[(request.session_id, request.action)] = _orchestrator.sessions[request.session_id].pending_actions.get(request.action)
    return {"status": "ok", "message": message, "action": request.action, "value": request.value}


@app.post("/actions/decide")
def decide(request: DecisionRequest) -> dict[str, Any]:
    key = (request.session_id, request.action)
    item = _pending.get(key)
    if item is None:
        item = _orchestrator.sessions.get(request.session_id, type("S", (), {"pending_actions": {}})()).pending_actions.get(request.action)
    if item is None:
        raise HTTPException(status_code=404, detail="No pending action found")
    if item.approval is None:
        return {"status": "ok", "executed": False, "message": "Action does not require approval."}
    item.approval.approved = bool(request.approved)
    if not request.approved:
        return {"status": "rejected", "executed": False}
    from .agents.workflow import execute_approved
    executed = execute_approved(item)
    return {"status": "approved", "executed": executed}


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard() -> str:
    pending_rows = []
    for (session_id, action), item in _pending.items():
        approval = getattr(item, "approval", None)
        if approval is not None and not approval.approved:
            pending_rows.append(
                f"<tr><td>{html.escape(session_id)}</td><td>{html.escape(action)}</td><td>{html.escape(item.description)}</td><td>{item.value if item.value is not None else ''}</td></tr>"
            )
    rows = "".join(pending_rows) or "<tr><td colspan='4'>لا توجد موافقات معلّقة</td></tr>"
    return f"""<!doctype html><html lang='ar' dir='rtl'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Hamed AI</title><style>body{{font-family:Arial,sans-serif;max-width:1100px;margin:40px auto;padding:0 20px}}table{{width:100%;border-collapse:collapse}}th,td{{padding:10px;border:1px solid #ddd;text-align:right}}.ok{{font-weight:700}}</style></head><body><h1>Hamed AI</h1><p>الحالة: <span class='ok'>تشغيل</span></p><p>مزود الذكاء: <span class='ok'>{'OpenAI' if settings.openai_api_key else 'Fallback مجاني'}</span></p><h2>الموافقات المعلّقة</h2><table><thead><tr><th>Session</th><th>Action</th><th>Description</th><th>Value</th></tr></thead><tbody>{rows}</tbody></table><p><a href='/docs'>API Docs</a> | <a href='/health'>Health</a></p></body></html>"""


def run_telegram_bot() -> None:
    """Compatibility hook; Telegram remains optional until its adapter is configured."""
    raise RuntimeError("Telegram adapter is not configured in this entrypoint. Use /chat or configure a dedicated adapter.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=False)
