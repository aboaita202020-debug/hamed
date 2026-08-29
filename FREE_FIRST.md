# Hamed AI — Free-First Mode

Hamed prefers local/open-source components and free tiers before paid APIs.

## Default

- `HAMED_FREE_MODE=true`
- `HAMED_ENABLE_PAID_APIS=false`
- No paid provider should be called unless explicitly enabled.

## Keep free/local

Research orchestration, website audit logic, sales planning, negotiation rules, CRM data, learning records, scoring and prompt templates should run locally or with open-source tooling whenever practical.

## Free website audit

`app/free_tools/website_scanner.py` is a dependency-free baseline audit using Python's standard library. It checks observable page-level signals including title, meta description, H1 structure, image alt text, and basic conversion-path signals. Findings are evidence-first and are not presented as a full browser-performance or technical-SEO audit.

## Voice

Real PSTN phone calls are not inherently free. For testing, Twilio currently advertises a 30-day trial with 75 voice minutes, verified-recipient restrictions, and a 10-minute per-call limit. Production PSTN usage must therefore be treated as a separately budgeted adapter. 

## Cost control

Use provider adapters so Hamed can switch between:

1. local/open-source speech and LLM components;
2. free/trial quotas;
3. paid APIs only when explicitly enabled.

Never place API keys in source control.
