"""
FastAPI Dashboard/Health/Webhook adapter — spec sections 19, 21, 25.

Reproduces the endpoints already seen in the original project
(section 22): /health and /dashboard, plus /webhook/telegram for a
production webhook deployment (vs. polling in scripts/run_telegram.py).

Optional on purpose: requires `fastapi` + `uvicorn` (see
requirements.txt). If they are missing, `create_app()` raises a clear
RuntimeError instead of an ImportError deep in someone else's code.
"""
from __future__ import annotations

from app.agents.orchestrator import HamedOrchestrator
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

    orch = orchestrator or HamedOrchestrator()
    app = FastAPI(title="Hamed AI", version="0.1.0")

    @app.get("/health")
    async def health():
        return {"status": "ok", "app": "Hamed AI"}

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
        return {
            "agent": outcome.agent,
            "attempts": outcome.attempts,
            "success": outcome.result.success,
            "error": outcome.result.error,
            "data": _jsonable(outcome.result.data),
        }

    @app.post("/webhook/telegram")
    async def telegram_webhook(request: Request):
        # Intentionally minimal: production Telegram webhook wiring is a
        # thin translation layer (see app/channels/telegram_adapter.py for
        # the polling variant used in development).
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
