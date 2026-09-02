# Hamed AI — Runny Deployment Instructions

## Required before first deployment

Runny should ask for exactly:

- `TELEGRAM_BOT_TOKEN`
- `OPENAI_API_KEY`

## Optional integrations

The following must NOT block a Telegram deployment when empty:

- `DATABASE_URL`
- all `TWILIO_*` variables
- all `PAYMOB_*` variables
- all additional AI-provider API keys

If an optional provider/integration has no credentials, it must simply be disabled or skipped.

## AI brains

Additional provider keys are optional. Hamed's router should use configured providers and fall back to available providers. Missing keys are not deployment errors.

## Security

Never use fake credentials to satisfy deployment prompts. Never commit real secrets to Git. Store credentials only in the deployment platform's secret/environment-variable storage.

## Telegram-first launch

A valid Telegram token plus an OpenAI key is sufficient for the standalone Telegram runtime. Database, Twilio voice, Paymob payments, and additional AI providers can be enabled later without changing the baseline deployment contract.

See `deploy/runny-deployment.yaml` for the machine-readable contract.
