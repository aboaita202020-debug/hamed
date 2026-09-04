# Hamed AI — Conversation & Project Context

> This document preserves the implementation context, decisions, requirements, constraints, and current state discussed for Hamed AI. It is intended as persistent project context for future coding/agent work.
>
> **Security:** No real secrets, API keys, passwords, payment credentials, or private financial data belong in this file. Use environment variables and placeholders.

## 1. Project Identity

- Project: **Hamed AI (حامد)**
- Repository: `aboaita202020-debug/hamed`
- Primary goal: build an autonomous commercial AI agent that finds legitimate revenue opportunities, sells, buys, negotiates, generates leads, manages follow-ups, and coordinates specialized agents.
- Target markets: Egypt, Gulf countries, and broader Arab markets.
- User preference: implementation first, minimal back-and-forth, test before launch, and prefer free/low-cost infrastructure where practical.
- Revenue is never guaranteed; Hamed must track opportunities and outcomes honestly.

## 2. Core Hamed Mission

Hamed is intended to operate as a commercial AI agent and manager of specialized agents. It should:

- Hunt for legitimate customers and opportunities.
- Act as a sales representative and purchasing agent.
- Research suppliers, products, prices, offers, and market gaps.
- Compare purchase price, expected sale price, margin, fulfillment, and risk.
- Build truthful offers and negotiate inside configured limits.
- Generate and recover qualified leads.
- Support affiliate marketing and referral revenue where lawful and transparent.
- Offer website/marketing/business services to appropriate prospects.
- Reactivate warm customers.
- Use buyer-first commercial workflows: find demand before sourcing supply when useful.
- Track cash velocity and time-to-cash.
- Coordinate multiple specialized AI agents/brains.
- Support Telegram, WhatsApp, voice, and social research when properly configured and legally/technically available.

## 3. Autonomous Operation Policy

Hamed should operate autonomously within configured limits without repeatedly asking the owner for routine actions.

However, major financial, irreversible, high-risk, or legally binding actions remain blocked unless explicit authorization is available.

Examples that must remain protected:

- Transfers of money.
- High-impact financial actions outside configured limits.
- Binding contracts.
- Account/security changes.
- Irreversible operations.
- Sensitive actions that require trusted human authorization.

Autonomy must never become a bypass around authorization or compliance.

## 4. Revenue Engine

The project has a unified Revenue Engine / Revenue OS concept that ranks legitimate commercial paths.

Important revenue routes include:

1. Warm customer reactivation.
2. Approved/public budget opportunities.
3. Ready-to-buy demand.
4. Buyer-first sourcing.
5. Legitimate arbitrage/price-gap opportunities.
6. Qualified lead monetization.
7. B2B brokerage.
8. Affiliate marketing.
9. Website services.
10. Marketing services.
11. Upsell/cross-sell.
12. Referral revenue.
13. Opportunity leasing and related commercial models where lawful.
14. Demand mining and market-gap detection.
15. Dead-capacity marketplace / reverse-RFP style opportunities.
16. Revenue recycling and portfolio management.

No feature may promise guaranteed income or fabricate customers, budgets, orders, or payment evidence.

## 5. Cash Velocity / Time-to-Cash

The Cash Velocity Engine prioritizes opportunities by realistic speed to collection while preserving compliance.

Priority order:

1. Warm Money / previous customers.
2. Approved/Public Budget opportunities.
3. Ready-to-Buy urgent demand.
4. Buyer First.
5. Arbitrage.
6. Qualified Lead Sale.

Five gates:

- Decision Speed.
- Payment Ready.
- Fulfillment Ready.
- Profit Guard.
- Trust/Compliance.

Important principles:

- Measure **Cash Collected Today**, not only deal value.
- Use Time-to-Cash Score based on decision proximity, payment readiness, fulfillment readiness, close probability, and margin, while penalizing approvals, delays, and risk.
- Maintain separate **Cash Now** and **Big Money** lists so large slow opportunities do not block fast opportunities.
- A 24-hour revenue sprint should prioritize warm customers, approved opportunities, ready-to-buy, buyer-first, arbitrage, then lead monetization according to Time-to-Cash + Expected Profit + Probability.
- Deposit-first commercial structures may be suggested as legitimate options, e.g. a reasonable upfront amount with the remainder on delivery, subject to the actual deal terms.

## 6. Opportunity Evidence & Compliance

Hamed may only use opportunity information it is authorized to access.

Do not infer, expose, or fabricate:

- Private balances.
- Confidential budgets.
- Private financial records.
- Non-public customer information.
- Unauthorized personal data.

The External Compliance Checkpoint was added because the Trust/Compliance gate must not simply self-certify high-risk decisions.

For high-value or repeated opportunities, the system should support a review state/queue and an external approval signal before execution.

Best-practice interpretation:

- Human review should be the authoritative approval path unless an explicitly configured trusted automated authority is used.
- Reviewer identity, timestamp, decision, reason, and relevant audit data should be recorded.
- Automated prechecks may assist but must not silently become the authority unless explicitly configured.

## 7. Autonomous Execution

The autonomous execution pipeline is designed around evidence-backed, bounded, reversible commercial work.

Typical stages:

- Verify evidence.
- Hunt opportunities.
- Generate leads.
- Build truthful offers.
- Price within configured bounds.
- Select the best revenue route.
- Contact an appropriate prospect/channel.
- Negotiate within configured limits.
- Recover eligible lost opportunities without spam.
- Follow up without spam.
- Request eligible referrals transparently.
- Measure funnel and profit metrics.

Voice calls must only target explicitly eligible/allowlisted prospects and must respect opt-outs and applicable rules.

## 8. Multiple Agents / AI Brains

The user wants Hamed to coordinate many specialized agents/brains. Counts discussed evolved from 4–5 to 10+, then 15–20, 40, and up to 80 specialized agents.

Specializations discussed include:

- Sales.
- Purchasing.
- Negotiation.
- Affiliate marketing.
- Lead generation.
- Customer discovery.
- Social research.
- Market research.
- Pricing.
- Psychology/customer understanding.
- Education/learning.
- Follow-up and CRM.
- Supplier discovery.
- Opportunity hunting.
- Revenue tracking.
- Compliance/risk.
- Voice/customer communications.

The architecture should prefer modular agents coordinated by an orchestrator rather than a monolithic prompt.

## 9. Social / Customer Discovery

Hamed should be able to identify legitimate opportunities and customers from public or authorized sources, including social platforms when integrations permit.

Requirements:

- Do not spam.
- Do not impersonate people or companies.
- Do not fabricate engagement or testimonials.
- Respect platform rules and opt-outs.
- Use only data Hamed is allowed to access.
- Lead generation should favor relevant, evidence-backed prospects.

## 10. Voice / WhatsApp / Telegram

The project has discussed:

- Telegram bot operation.
- WhatsApp communication.
- Outbound voice calls.
- AI voice responses.

Voice-call controller requirements:

- Credentials must remain in environment variables.
- Outbound targets must be explicitly allowlisted.
- Attempt counts must be policy-limited.
- Caller ID should use the configured business number.
- A public HTTPS base URL is required for Twilio webhooks.
- Real Twilio calls are **not considered live** unless credentials and the required public endpoint are actually configured and tested.

Telegram bot environment:

- `TELEGRAM_BOT_TOKEN` required for the bot.
- `OPENAI_API_KEY` required where OpenAI intelligence is enabled.
- `DATABASE_URL` optional.
- Twilio variables optional unless voice is enabled.
- Paymob variables optional unless payment integration is enabled.

## 11. Manual Payment / Vodafone Cash — Current Security Design

Initial payment flow is intentionally manual and should not claim automatic Vodafone Cash integration.

Flow:

1. Hamed creates a payment request.
2. Customer receives the exact amount, currency, payment method, configured Vodafone Cash number, reference code, and instructions.
3. Customer transfers money.
4. Customer submits proof or transaction number.
5. Payment enters `submitted` then `under_review`.
6. An authorized reviewer receives a Telegram notification.
7. A trusted reviewer manually confirms or rejects.
8. Only `confirmed` may trigger fulfillment and revenue recognition.

Required payment statuses:

- `pending`
- `submitted`
- `under_review`
- `confirmed`
- `rejected`
- `expired`

Payment request fields should include:

- `payment_id`
- `customer_id` / `chat_id` / `user_id`
- amount
- currency = EGP
- `payment_method = vodafone_cash`
- unique reference code
- status
- created timestamp
- expiry timestamp
- confirmation data

Environment variable:

- `HAMED_VODAFONE_CASH_NUMBER`

Never commit a real Vodafone Cash number to Git. Keep it in the environment only.

### Critical Manual Payment Security Rules

1. Screenshot or transaction number is **not automatic proof of payment**.
2. Customer submission cannot confirm payment.
3. Confirmation must require trusted reviewer authorization.
4. `HAMED_PAYMENT_REVIEWER_IDS` must be fail-closed.
5. Missing or empty reviewer configuration must block confirmation.
6. A `reviewer_id` supplied by an untrusted request body is not authentication.
7. If real authentication is unavailable, confirmation must remain blocked in production.
8. Never create a fake security workaround merely to make tests pass.
9. Forbidden workarounds include hardcoded reviewer secrets, static tokens in source, hardcoded passwords, simple text comparisons presented as authentication, or test-only bypasses.
10. Reviewer impersonation must be blocked.
11. Confirmation/rejection must create audit events with reviewer identity, timestamp, payment ID, amount, currency, reference code, decision, and note/reason.
12. Notification failure must not result in confirmation.
13. Amount must be immutable after payment creation.
14. Direct status manipulation must be blocked.
15. Double confirmation must be blocked.
16. Customers cannot confirm payments or access other customers' payment records.
17. Revenue and fulfillment remain blocked until `confirmed`.

### Payment API

Expected endpoints:

- `POST /payments/create`
- `POST /payments/{payment_id}/submit`
- `POST /payments/{payment_id}/confirm`
- `POST /payments/{payment_id}/reject`
- `GET /payments/{payment_id}`

### Reviewer Notification

When a payment enters `under_review`, send a Telegram notification containing only the minimum necessary information:

- payment ID
- amount
- currency
- reference code
- non-sensitive customer identifier
- timestamp
- status

If notification fails, confirmation must remain blocked and the failure should be logged/audited.

### Payment Provider Abstraction

Keep a `PaymentProvider` abstraction so future Paymob/Accept integration can be added without rebuilding manual-payment state logic.

## 12. Required Payment Tests

At minimum, tests should cover:

1. Payment creation.
2. Unique reference code.
3. Submit flow.
4. Screenshot does not confirm payment.
5. State-transition validation.
6. Missing reviewer configuration → blocked.
7. Empty reviewer allowlist → blocked.
8. Unauthorized reviewer → blocked.
9. Reviewer impersonation → blocked.
10. Unauthenticated reviewer identity → blocked.
11. No fake/static-token authentication workaround.
12. Double confirmation → blocked.
13. Amount modification → blocked.
14. Direct status modification → blocked.
15. Fulfillment before confirmation → blocked.
16. Revenue before confirmation → blocked.
17. Audit event creation.
18. Telegram reviewer notification.
19. Notification failure → confirmation remains blocked.
20. Reject flow.
21. Expiration flow.
22. Sensitive secrets absent from logs.
23. Customer cannot confirm payment.
24. Customer cannot access another customer's payment.

## 13. External Compliance Checkpoint

The external compliance checkpoint exists to prevent Hamed from being the sole authority on sensitive high-value/repeated commercial actions.

Expected behavior:

- Normal low-risk opportunities can proceed according to policy.
- High-value/repeated opportunities can enter `pending_review`.
- Execution remains blocked until the required external approval is present.
- Review activity is auditable.
- Thresholds should be configurable through environment/configuration.

Do not weaken this gate just to improve autonomous conversion.

## 14. Audit Requirements

Structured audit events should capture at least:

- actor
- action
- status
- details
- timestamp

Sensitive credentials and secrets must never be written to logs.

## 15. CI / Testing

The repository has a GitHub Actions test workflow intended to run:

- dependency installation
- Python syntax check
- full pytest suite
- Docker build
- Docker health smoke test

The Docker smoke test should start the container with test placeholders and verify `/health` on port 8000.

Important: a GitHub status of `pending` with no completed statuses must not be described as passing.

## 16. Known Runtime Context

Previous local environment:

- Windows 7.
- Python 3.8.10.
- Previously observed dashboard: `http://127.0.0.1:8000/dashboard`.
- Previously observed health endpoint: `http://127.0.0.1:8000/health`.

A previous server message indicated that the basic server was running while advanced intelligence required an AI provider connection.

Prior technical problems included:

- missing `HamedOrchestrator` import.
- missing `package.json` / Node tooling mismatch.
- GitHub Actions failures.
- Docker readiness failures.
- Twilio verification/credentials issues.
- Need to test before deployment.

## 17. GitHub Development State

Repository:

`aboaita202020-debug/hamed`

A revenue-focused working branch has been used:

`feat/revenue-money-machine-v2`

An open PR was previously used:

`PR #7` targeting `main`.

Relevant historical commits included Revenue/Cash Velocity and External Compliance Checkpoint changes. Always inspect the actual current branch/PR state before claiming a feature exists; historical commit IDs are context, not proof of current deployment.

## 18. Deployment Philosophy

Preferred order:

1. Implement.
2. Run syntax checks.
3. Run unit/integration tests.
4. Run Docker/build smoke tests where applicable.
5. Review security and authorization.
6. Fix failures.
7. Only then deploy.

Do not declare production readiness from a green-looking report alone. Inspect actual code, tests, CI status, and security boundaries.

## 19. User's Working Style / Execution Preference

The user strongly prefers:

- direct execution instead of repeated clarification
- complete implementation where safe
- tests before launch
- fixing errors rather than explaining them repeatedly
- practical results
- concise Egyptian Arabic updates

When a sensitive authorization or real-money blocker genuinely exists, explain it clearly instead of silently bypassing it.

## 20. Non-Negotiable Safety / Integrity Rules

Hamed must never:

- fabricate sales or payment confirmations
- claim guaranteed revenue
- impersonate customers, reviewers, or companies
- bypass authentication
- bypass payment review
- access private financial information without authorization
- spam prospects
- ignore opt-outs
- create fake testimonials or engagement
- store secrets in Git
- use fake security mechanisms just to satisfy tests
- execute high-impact irreversible financial actions without required authorization

## 21. Current Strategic Objective

Build Hamed into a practical autonomous commercial operating system that continuously searches for legitimate revenue opportunities, ranks them by time-to-cash and expected profit, executes bounded commercial actions automatically, and stops for trusted human authorization whenever security, compliance, or financial impact requires it.

The goal is not merely to make Hamed "look intelligent". The goal is a measurable system with:

- evidence-backed opportunities
- real customer discovery
- transparent offers
- controlled negotiation
- secure payment states
- auditable decisions
- measurable revenue outcomes
- strong fail-closed authorization
- repeatable automated execution
