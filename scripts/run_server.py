"""
Production entrypoint for the FastAPI dashboard/health/webhook/chat server.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.agents.orchestrator import HamedOrchestrator
from app.agents.provider import MultiBrainProvider
from app.api.server import create_app

brain_provider = MultiBrainProvider()
orchestrator = HamedOrchestrator(brain_provider=brain_provider)
app = create_app(orchestrator)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.host, port=settings.port)
