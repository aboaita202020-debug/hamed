"""
Production entrypoint for the FastAPI dashboard/health/webhook server.

Usage:
    python scripts/run_server.py
Or on Render, as a Start Command:
    uvicorn scripts.run_server:app --host 0.0.0.0 --port $PORT

Requires: pip install -r requirements.txt (fastapi, uvicorn)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.agents.orchestrator import HamedOrchestrator
from app.api.server import create_app

orchestrator = HamedOrchestrator()
app = create_app(orchestrator)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.host, port=settings.port)
