# 🤖 Hamed AI

Hamed is an AI commercial operating system evolving from the original Telegram/Claude MVP into a modular sales, purchasing, research, negotiation, finance, customer-service and website-assistance platform.

## Current implementation
- AI provider abstraction with OpenAI as the primary provider.
- Hamed orchestration layer with conversational session memory.
- Deterministic commercial calculations for landed cost, revenue, gross profit and margin.
- Server-side approval primitives for high-impact actions.
- Structured audit events.
- Telegram MVP remains in the repository during migration.

## Security rules
- Never commit `.env` or real API keys.
- Research and drafting can be autonomous; purchases, payments, contracts, publishing and irreversible actions require explicit approval.
- The model must never bypass server-side authorization.
- Unknown commercial inputs must be presented as unknown/estimated, not invented.

## Local setup
1. Copy `.env.example` to `.env` and add your credentials.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Run tests:
   `pytest -q`
4. The legacy Telegram entry point is `python bot.py` while the migration continues.

## Roadmap
See `HAMED_AI_CODEX.md` for the complete architecture, agent roles, approval policy, channels, seller website workflow, dashboard, testing strategy and production delivery phases.
