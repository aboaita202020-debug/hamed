"""Unified Hamed AI application entrypoint."""
from __future__ import annotations

import html
import os
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .agent_worker import HamedWorker
from .agents.commercial_brain import build_plan
from .agents.orchestrator import HamedOrchestrator
from .agents.provider import OpenAIProvider
from .config import settings
from .runtime import http_host, http_port


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


app = FastAPI(title="Hamed AI", version="0.5.0", docs_url="/docs")
_provider = OpenAIProvider(settings.openai_api_key, settings.openai_model) if settings.openai_api_key else FallbackProvider()
_orchestrator = HamedOrchestrator(_provider)
_worker = HamedWorker(interval_seconds=int(os.getenv("HAMED_WORKER_INTERVAL", "900")))
_pending: dict[tuple[str, str], Any] = {}


def autonomous_scan() -> dict[str, Any]:
    """Create the next safe commercial work agenda; no spending/publishing/calls occur here."""
    prompt = (
        "حدد أولويات العمل التجاري الآمن لحامد الآن. ركّز بالترتيب على: "
        "اكتشاف فرص خدمات مواقع ومتاجر، فرص تسويق بالعمولة عالية الملاءمة، "
        "فرص شراء وإعادة بيع، ثم تحسين مهارات البيع والتفاوض. "
        "أخرج 3 مهام عملية قابلة للبحث أو التحليل، بدون شراء أو دفع أو نشر أو تعاقد."
    )
    plan = build_plan(prompt)
    return {
        "status": "ok",
        "task_type": "commercial_scan",
        "objective": plan.objective.value,
        "next_steps": plan.next_steps,
        "requires_research": plan.requires_research,
        "approval_required": plan.approval_required,
        "safe_mode": True,
    }


@app.on_event("startup")
async def start_worker() -> None:
    if os.getenv("HAMED_WORKER_ENABLED", "true").lower() == "true":
        _worker.start(hooks=[autonomous_scan])


@app.on_event("shutdown")
async def stop_worker() -> None:
    _worker.stop()


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
        "worker": _worker.status(),
    }


@app.get("/worker/status")
def worker_status() -> dict[str, Any]:
    return _worker.status()


@app.post("/worker/run")
def worker_run() -> dict[str, Any]:
    return _worker.run_once(hooks=[autonomous_scan])


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


@app.get("/dashboard/data")
def dashboard_data() -> dict[str, Any]:
    pending = []
    for (session_id, action), item in _pending.items():
        approval = getattr(item, "approval", None)
        if approval is not None and not approval.approved:
            pending.append({
                "session_id": session_id,
                "action": action,
                "description": getattr(item, "description", ""),
                "value": getattr(item, "value", None),
            })
    return {"pending_approvals": pending, "count": len(pending)}


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard() -> str:
    ui_path = os.path.join(os.path.dirname(__file__), "ui", "dashboard.html")
    if os.path.exists(ui_path):
        with open(ui_path, "r", encoding="utf-8") as fh:
            return fh.read()
    return "<h1>Hamed AI</h1><p>واجهة التحكم غير متاحة حاليًا.</p>"


def run_telegram_bot() -> None:
    """Compatibility hook; Telegram remains optional until its adapter is configured."""
    raise RuntimeError("Telegram adapter is not configured in this entrypoint. Use /chat or configure a dedicated adapter.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=http_host(),
        port=http_port(),
        reload=False,
    )
