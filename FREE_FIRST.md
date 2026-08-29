# Hamed AI — Free-First Mode

Hamed is configured to prefer local/open-source components and free tiers before paid APIs.

## Default

- `HAMED_FREE_MODE=true`
- `HAMED_ENABLE_PAID_APIS=false`
- No paid provider should be called unless explicitly enabled.

## Keep free/local

Research orchestration, website audit logic, sales planning, negotiation rules, CRM data, learning records, scoring and prompt templates should run locally or with open-source tooling whenever practical.

## Voice

Real PSTN phone calls are not inherently free. A trial provider can be used for testing. Twilio currently advertises 75 trial voice minutes for a 30-day trial, with verified-recipient and other restrictions. Trial Media Streams are restricted, so a fully free production PSTN voice stack should not be assumed.

## Cost control

Use a provider adapter so Hamed can switch between:

1. local/open-source speech and LLM components;
2. free/trial quotas;
3. paid APIs only when explicitly enabled.

Never place API keys in source control.
