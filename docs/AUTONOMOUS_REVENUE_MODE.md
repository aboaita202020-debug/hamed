# Hamed Autonomous Revenue Mode

Hamed is designed to operate independently on routine commercial work with the goal of increasing legitimate revenue and customer value.

## Autonomous capabilities

- Sales conversations and follow-up.
- Negotiation within configured commercial limits.
- Affiliate marketing and lead generation.
- Supplier/product research and opportunity ranking.
- Website and e-commerce service sales.
- Customer-service workflows.
- Commercial calculations, pricing suggestions, and performance analysis.
- Telegram reporting.

## Server-enforced boundaries

The language model cannot grant itself permissions. The execution guard remains outside the model and enforces the policy.

Routine commercial actions can run autonomously when `HAMED_AUTONOMOUS_MODE=true`.

Purchases and payment actions require explicit numeric server limits:

- `HAMED_MAX_PURCHASE_VALUE`
- `HAMED_MAX_PAYMENT_VALUE`

High-risk actions and irreversible/account/legal actions remain blocked from model-only authorization.

## Vodafone Cash

Vodafone Cash is already represented as a customer payment option and has a dedicated adapter. The merchant wallet must be supplied through `HAMED_VODAFONE_CASH_WALLET`; the wallet number must never be hard-coded or committed to Git.

The current adapter creates payment instructions and only confirms payment after a trusted verification step. It does not request customer wallet PINs or OTPs.

## Telegram

Configure `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` as deployment secrets. Never commit either value.
