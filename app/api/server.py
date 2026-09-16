from __future__ import annotations

from app.agents.orchestrator import HamedOrchestrator
from app.agents.provider import MultiBrainProvider
from app.agents.smart_minds import list_smart_minds
from app.logging_config import get_logger

logger = get_logger(__name__)

try:
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
    _FASTAPI_AVAILABLE = True
except ImportError:  # pragma: no cover
    _FASTAPI_AVAILABLE = False


def create_app(orchestrator: HamedOrchestrator | None = None):
    if not _FASTAPI_AVAILABLE:
        raise RuntimeError("fastapi/uvicorn not installed. Run: pip install fastapi uvicorn")
    orch = orchestrator or HamedOrchestrator(brain_provider=MultiBrainProvider())
    app = FastAPI(title="Hamed AI", version="0.1.0")

    @app.get("/health")
    async def health():
        return {"status": "ok", "app": "Hamed AI", "smart_minds": len(list_smart_minds())}

    @app.get("/readiness")
    async def readiness():
        try:
            orch.repo.dashboard_snapshot()
            return {"status": "ready"}
        except Exception as exc:
            return JSONResponse(status_code=503, content={"status": "not_ready", "error": str(exc)})

    @app.get("/dashboard")
    async def dashboard():
        return orch.dashboard()

    @app.get("/smart-minds")
    async def smart_minds():
        minds = list_smart_minds()
        return {"status": "ok", "count": len(minds), "minds": minds}

    @app.get("/agent-runs")
    async def agent_runs(limit: int = 25):
        limit = max(1, min(limit, 100))
        return orch.repo.list_agent_runs(limit=limit)

    @app.post("/chat")
    async def chat(request: Request):
        payload = await request.json()
        message = str(payload.get("message", "")).strip()
        if not message:
            return JSONResponse(status_code=400, content={"status": "error", "error": "message_required"})
        if orch.brain_council is None:
            return JSONResponse(status_code=503, content={"status": "error", "error": "brain_provider_not_configured"})
        context = str(payload.get("context", ""))
        roles = payload.get("roles")
        if roles is not None and not isinstance(roles, list):
            return JSONResponse(status_code=400, content={"status": "error", "error": "roles_must_be_list"})
        try:
            result = orch.consult_brains(message, context=context, roles=roles)
            return {"status": "ok", "message": message, **result}
        except Exception as exc:
            logger.exception("Chat request failed")
            return JSONResponse(status_code=502, content={"status": "error", "error": str(exc)})

    @app.get("/leads")
    async def leads(stage: str | None = None):
        rows = orch.repo.list_leads(stage=stage)
        return [r.__dict__ for r in rows]

    @app.get("/opportunities")
    async def opportunities(min_score: float = 0.0):
        rows = orch.repo.list_opportunities(min_score=min_score)
        return [r.__dict__ for r in rows]

    @app.get("/audit-logs")
    async def audit_logs(limit: int = 100):
        return orch.repo.list_audit_logs(limit=limit)

    @app.post("/dispatch/{agent_name}")
    async def dispatch(agent_name: str, request: Request):
        payload = await request.json()
        outcome = orch.dispatch(agent_name, payload)
        return {"agent": outcome.agent, "attempts": outcome.attempts, "success": outcome.result.success, "error": outcome.result.error, "data": _jsonable(outcome.result.data)}

    @app.post("/webhook/telegram")
    async def telegram_webhook(request: Request):
        payload = await request.json()
        logger.info("Received Telegram webhook update: %s", str(payload)[:200])
        return {"ok": True}

    return app


def _jsonable(value):
    if hasattr(value, "__dict__"):
        return value.__dict__
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    return value
