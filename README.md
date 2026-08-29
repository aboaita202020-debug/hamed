# 🤖 Hamed AI

Hamed is an AI commercial operating system evolving from the original Telegram/Claude MVP into a modular sales, purchasing, research, negotiation, finance, customer-service and website-assistance platform.

## 🚀 One-click Koyeb deployment

Use the official Koyeb deployment flow for this public GitHub repository:

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&builder=docker&repository=github.com/aboaita202020-debug/hamed&branch=main&name=hamed-ai&ports=8000%3Bhttp%3B%2F)

This opens Koyeb with Hamed preconfigured from the `main` branch and the repository Dockerfile. You still need to sign in to Koyeb and authorize the deployment from your own account.

## Current implementation
- AI provider abstraction with OpenAI as the primary provider.
- Hamed orchestration layer with conversational session memory.
- Deterministic commercial calculations for landed cost, revenue, gross profit and margin.
- Server-side approval primitives for high-impact actions.
- Structured audit events.
- Commercial learning engine for sales, purchasing, negotiation, affiliate marketing, services, websites and stores.
- Voice bridge architecture for Twilio + OpenAI Realtime.
- Local Windows server and cloud deployment configurations.
- Telegram MVP remains in the repository during migration.

## Security rules
- Never commit `.env` or real API keys.
- Research and drafting can be autonomous; purchases, payments, contracts, publishing and irreversible actions require explicit approval.
- The model must never bypass server-side authorization.
- Unknown commercial inputs must be presented as unknown/estimated, not invented.
- Voice calls must follow the configured allowlist/permission policy.

## Local setup
1. Copy `.env.example` to `.env` and add your credentials only when required.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Run tests:
   `pytest -q`
4. Local server:
   `python local_server.py`
5. The legacy Telegram entry point is `python bot.py` while the migration continues.

## Production/cloud setup
See:
- `HAMED_AI_CODEX.md` for the complete architecture and execution specification.
- `FREE_FIRST.md` for the low-cost/free-first strategy.
- `DEPLOY_FREE.md` and `deploy/oracle/` for Oracle Cloud deployment.
- `deploy/koyeb/` for Koyeb deployment.
- `app/voice/` for the voice agent integration.

## Important
The free hosting layer does not make third-party AI inference or telephone carrier minutes unlimited/free. Keep paid integrations disabled until the project has revenue or an explicit budget, then enable them with server-side limits and approval controls.
