"""
Development entrypoint: runs the Telegram bot with polling (no public
URL needed). For production, prefer the /webhook/telegram route in
scripts/run_server.py behind a real domain.

Usage:
    python scripts/run_telegram.py

Requires: TELEGRAM_BOT_TOKEN set, and
    pip install 'python-telegram-bot>=20,<21'
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.agents.orchestrator import HamedOrchestrator
from app.channels.telegram_adapter import build_telegram_app
from app.logging_config import get_logger

logger = get_logger("run_telegram")

if __name__ == "__main__":
    orchestrator = HamedOrchestrator()
    try:
        telegram_app = build_telegram_app(orchestrator)
    except RuntimeError as exc:
        logger.error(str(exc))
        sys.exit(1)

    logger.info("Hamed AI Telegram bot starting (polling mode)...")
    telegram_app.run_polling()
