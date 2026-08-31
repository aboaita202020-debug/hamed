# Hamed AI — Multi-Brain Configuration

Hamed supports a provider-neutral brain layer. Add only the API keys you have; the router automatically uses the configured providers.

## Providers

- OpenAI: `OPENAI_API_KEY`, `OPENAI_MODEL`
- Claude/Anthropic: `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL`
- DeepSeek: `DEEPSEEK_API_KEY`, `DEEPSEEK_MODEL`, optional `DEEPSEEK_BASE_URL`
- Kimi/Moonshot: `KIMI_API_KEY`, `KIMI_MODEL`, optional `KIMI_BASE_URL`

## Routing

`HAMED_AI_PROVIDERS=openai,claude,deepseek,kimi`

The order controls fallback priority. Use `HAMED_AI_MODE=fallback` for resilient routing. Use `HAMED_AI_MODE=council` to ask every configured brain and have the first configured brain synthesize the candidates.

## Security

Never commit API keys or Telegram tokens. Store them in deployment secrets/environment variables. Model output never receives permission to alter these credentials.

## Operational principle

Multiple models are specialists, not independent authorities. Hamed's deterministic workflow, payment rules, approval boundaries, and execution tools remain the control plane; model output is advisory/decision-support input to that control plane.
