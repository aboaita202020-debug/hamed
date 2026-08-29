# Hamed AI — Free-First Cloud Deployment

## Goal
Run Hamed continuously on a cloud VM without depending on the user's phone or PC. Keep fixed infrastructure cost at zero while validating the business; paid APIs are enabled only when revenue or an explicit budget exists.

## Recommended deployment
Oracle Cloud Always Free VM (availability and eligibility vary by region/account). The VM runs the Hamed application and webhook endpoint 24/7.

## Architecture
GitHub → Oracle Cloud VM → Hamed → OpenAI / Voice provider

The phone is only a control surface. Hamed continues running if the phone is offline.

## Required environment variables
Set these on the VM, never commit secrets:
- OPENAI_API_KEY
- TWILIO_ACCOUNT_SID
- TWILIO_AUTH_TOKEN
- TWILIO_FROM_NUMBER
- PUBLIC_BASE_URL

For a zero-spend development mode, omit live Twilio/OpenAI credentials and use mocks/local adapters. Real phone calls and hosted AI API usage may incur provider charges.

## Revenue gate
Use `HAMED_PAID_FEATURES_ENABLED=false` until the project has revenue or an approved budget. When enabled, paid voice/API features can be used subject to configured spending limits.

## Operational principles
1. No secrets in Git.
2. Start with verified/test numbers only.
3. Do not initiate unsolicited bulk calling.
4. Identify the AI agent when required.
5. Respect opt-outs and applicable telecom/privacy rules.
6. Keep human approval for high-impact financial commitments.
