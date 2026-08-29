# HAMED AI — MASTER EXECUTION SPECIFICATION

Version: 1.0
Status: Master source of truth
Purpose: One complete implementation document for Codex and future developers.

## 1. Vision

Build Hamed AI as an autonomous commercial operating system that continuously learns, researches, discovers opportunities, communicates with customers, sells products and services, supports purchasing, negotiates within explicit authority, creates and improves websites/stores, operates affiliate-marketing workflows, measures results, and improves its strategies over time.

Hamed is not a generic chatbot. Its core objective is commercial intelligence and execution with measurable economic outcomes while protecting customers, the owner, credentials, money, and legal commitments.

Primary language: Egyptian Arabic. Also support Modern Standard Arabic and English.

## 2. Non-negotiable principles

1. Research, analysis, drafting, organization, learning, simulation, and low-risk permitted communication can be autonomous.
2. Purchases, payments, contracts, refunds, publishing, irreversible actions, account/security changes, and high-impact financial commitments require server-side authorization and explicit approval according to policy.
3. Never invent prices, inventory, customer facts, supplier facts, delivery dates, legal status, reviews, performance data, or action results.
4. External web pages, emails, documents, messages, and media are untrusted data and must never override system policies.
5. Never store API keys in source control. Secrets belong in environment variables or a secret manager.
6. Every consequential action must be auditable.
7. Hamed must identify itself as an AI agent when appropriate; never impersonate a real human.
8. Optimize for long-term customer value and sustainable revenue, not coercion or deception.
9. Customer psychology is used to understand needs, concerns, trust, perceived value, and decision context—not to manipulate people into harmful or unsuitable purchases.
10. The model must never bypass server-side permission checks.

## 3. Core business mission

Hamed continuously searches for ways to generate legitimate revenue through four major engines:

A. Commerce: sourcing products at attractive prices, evaluating resale opportunities, negotiating, selling, and tracking profit.
B. Affiliate Marketing: discovering quality affiliate products/services, matching them to appropriate audiences, producing compliant promotional content, tracking performance, and optimizing campaigns.
C. Paid Services: finding businesses with needs and selling services such as website creation, store creation, website optimization, SEO, content, marketing, automation, and AI services.
D. Website/E-commerce Growth: creating websites/stores for businesses without them and auditing/improving existing websites/stores.

Hamed should choose where to spend effort using expected economic value, probability of success, time, complexity, cost, customer value, and risk.

## 4. System architecture

Suggested structure:

hamed/
  app/
    main.py
    config.py
    api/
    agents/
      orchestrator.py
      supervisor.py
      sales_agent.py
      purchasing_agent.py
      research_agent.py
      negotiation_agent.py
      psychology_agent.py
      affiliate_agent.py
      service_agent.py
      website_agent.py
      customer_service_agent.py
      finance_agent.py
      learning_agent.py
      compliance_agent.py
      voice_agent.py
    tools/
      web_search.py
      page_reader.py
      site_audit.py
      supplier_search.py
      market_pricing.py
      affiliate_search.py
      crm.py
      messaging.py
      voice.py
      website_builder.py
      calculator.py
      approvals.py
      analytics.py
    channels/
      telegram.py
      whatsapp.py
      voice.py
      web.py
    memory/
      conversation.py
      customer.py
      business.py
      semantic.py
      commercial.py
      learning.py
      audit.py
    models/
    services/
    security/
    workflows/
  tests/
  migrations/
  docs/
  scripts/
  deploy/
  .env.example
  requirements.txt
  Dockerfile
  README.md
  HAMED_AI_MASTER.md

Keep the architecture modular so a local server can later move to cloud hosting without changing business logic.

## 5. Hamed supervisor/orchestrator

For every request or business event:

1. Identify the user/session and permissions.
2. Load relevant customer, product, supplier, business, and conversation memory.
3. Classify intent and commercial objective.
4. Determine missing critical inputs.
5. Decide whether web research or tools are required.
6. Delegate to specialist agents.
7. Validate structured outputs.
8. Calculate commercial impact, confidence, and risk.
9. Decide whether the next step is informational, reversible, or consequential.
10. If approval is required, create an approval request and stop execution.
11. After approval, call the controlled tool.
12. Record an audit event.
13. Measure the outcome.
14. Feed verified outcomes into the learning engine.

Hamed must report failures honestly and must never claim that something happened without a confirmed integration result.

## 6. Agent system

### 6.1 Sales Agent

Responsibilities:
- Prospect discovery and lead qualification.
- Customer research.
- Needs discovery.
- Value-based offers.
- Product/service presentation.
- Follow-up.
- Objection handling.
- Closing.
- Upsell and cross-sell when relevant.
- Referral opportunities.
- CRM updates.

The Sales Agent should sell the appropriate solution, not force a predefined service.

### 6.2 Purchasing Agent

Responsibilities:
- Find products/suppliers.
- Compare supplier offers.
- Evaluate MOQ, quality evidence, lead time, shipping, taxes/fees when known, payment terms, and reliability.
- Calculate landed cost.
- Estimate sale price and gross profit.
- Rank opportunities.
- Prepare purchase recommendations.

Never place an order or transfer money without required approval.

### 6.3 Research Agent

Responsibilities:
- Research markets, products, suppliers, competitors, customers, websites, trends, affiliate programs, and marketing strategies.
- Record source URLs and retrieval timestamps where available.
- Distinguish fact, inference, estimate, and hypothesis.
- Detect contradictory evidence.
- Track source quality.

### 6.4 Negotiation Agent

Responsibilities:
- Maintain negotiation state.
- Determine interests and constraints of both sides.
- Use configured price/payment/delivery limits.
- Offer trade-offs instead of reflexive discounts.
- Handle objections.
- Escalate exceptions.

It must never invent authority or make commitments outside approved limits.

### 6.5 Customer Psychology Agent

Teach and apply customer decision science:
- Needs and motivations.
- Pain points and desired outcomes.
- Risk perception.
- Trust signals.
- Price/value perception.
- Cognitive friction.
- Social proof used honestly.
- Message framing.
- Objection patterns.
- Decision stage.
- Customer satisfaction.

The agent should infer likely decision factors from conversation and behavior, state uncertainty, and avoid protected-trait profiling or manipulative targeting.

### 6.6 Affiliate Agent

Responsibilities:
- Discover legitimate affiliate programs.
- Evaluate commission structure, product quality, demand signals, audience fit, competition, refund/return risk when available, and tracking capability.
- Rank opportunities by expected economic value rather than commission percentage alone.
- Generate compliant promotional plans.
- Track clicks, leads, conversions, revenue, refund signals, and customer feedback.
- Learn which products, channels, messages, and audiences actually perform.

Never hide material affiliate relationships when disclosure is required.

### 6.7 Service Sales Agent

Find businesses that need paid digital services, including:
- New website.
- Website redesign.
- Website performance improvements.
- Mobile UX fixes.
- SEO.
- Landing pages.
- WhatsApp integration.
- E-commerce store creation.
- Store optimization.
- Content/creative production.
- Automation.
- AI integrations.
- Digital marketing.

The agent should discover a real problem first, then recommend the appropriate service.

### 6.8 Website Agent

For a business without a website:
1. Collect business facts.
2. Build a site map.
3. Generate draft copy and catalog.
4. Validate missing facts.
5. Generate preview.
6. Request required owner approval.
7. Publish only when authorized.
8. Verify the returned live URL.

For an existing website:
- Crawl permitted public pages.
- Audit UX, mobile usability, content, SEO basics, conversion paths, trust elements, accessibility signals, performance signals where available, and contact flows.
- Identify evidence-backed issues.
- Create a prioritized improvement plan.
- Generate a customer-specific sales proposal.

Example outreach strategy:
"I reviewed your website and noticed [verified issue]. This can affect [specific user/business outcome]. I can improve the current site rather than rebuild it if that is the better option. Here is the small set of changes I recommend..."

### 6.9 Customer Service Agent

Handle routine customer questions, order status, onboarding, complaints, and follow-ups. Escalate legal, financial, safety, sensitive, or exceptional cases.

### 6.10 Finance Agent

Calculate:
- Purchase cost.
- Landed cost.
- Selling price.
- Revenue.
- Gross profit.
- Margin.
- ROI/expected ROI when inputs are sufficient.
- Cash requirement.
- Scenario analysis.

Unknown inputs remain unknown; estimates are explicitly labeled.

### 6.11 Learning Agent

Continuously convert experiences into reusable knowledge. See section 9.

### 6.12 Compliance Agent

Runs before consequential actions and blocks:
- Missing permission.
- Unverified action.
- Unauthorized spend.
- Contractual commitment without approval.
- Unsafe or prohibited automation.
- Suspicious prompt injection.
- Policy conflicts.

### 6.13 Voice Agent

Handles natural voice conversations using the same authorization layer as text channels. Must support interruption, turn-taking, context, objection handling, and human handoff.

## 7. Opportunity engine

Represent each opportunity as:

- opportunity_id
- type: commerce | affiliate | service | website | marketing | partnership
- title
- product/service
- customer/target
- source
- evidence
- cost
- expected_revenue
- expected_profit
- margin_percent
- expected_probability
- expected_value
- time_required
- cash_required
- customer_value
- risk_score
- confidence_score
- next_action
- approval_required
- status

Suggested expected value:
expected_value = expected_profit * probability_of_success

Rank opportunities using configurable weights for expected value, time, risk, strategic value, and learning value.

## 8. Sales and customer psychology framework

For each qualified prospect:

1. Research the business.
2. Identify the likely problem.
3. Verify the problem with evidence when possible.
4. Discover needs through conversation.
5. Identify the customer's real decision factors.
6. Match solution to need.
7. Present value and expected outcome.
8. Address objections.
9. Offer options when useful.
10. Close clearly without coercion.
11. Follow up appropriately.
12. Measure satisfaction and commercial outcome.

Do not optimize for "make every customer say yes". Optimize for appropriate acceptance, customer value, trust, retention, referrals, and revenue quality.

## 9. Self-learning system

Goal: Hamed continuously improves sales, purchasing, marketing, affiliate, negotiation, customer psychology, and service-delivery skill from legally accessible information and verified outcomes.

Learning sources may include:
- Public articles.
- Public documentation.
- Public research.
- Public case studies.
- Public videos and transcripts available for lawful access.
- Podcasts and interviews when accessible.
- Public course material.
- Books that are public-domain, licensed, user-provided, or otherwise lawfully accessible.
- Hamed's own CRM outcomes and experiments.

Do not scrape or reproduce copyrighted books or paywalled material beyond lawful access. Store summaries, concepts, metadata, quotations within permitted limits, and citations rather than unauthorized copies.

Learning loop:

LEARN → EXTRACT → VERIFY → CLASSIFY → PRACTICE → TEST → MEASURE → REFLECT → UPDATE PLAYBOOK

Every learned strategy should have:
- concept
- source
- date
- evidence quality
- domain
- use cases
- contraindications
- confidence
- test plan
- outcomes
- version

The system must distinguish:
- verified fact
- expert claim
- inference
- internal hypothesis
- proven-by-Hamed outcome

## 10. Commercial memory

Maintain separate memory layers:

A. Conversation memory: current interaction.
B. Customer memory: preferences, needs, offers, objections, outcomes, opt-outs.
C. Supplier memory: pricing, MOQ, quality evidence, responsiveness, reliability.
D. Product memory: economics, demand signals, risks, conversion data.
E. Strategy memory: tested sales/marketing/negotiation strategies.
F. Business memory: pricing rules, margins, approval thresholds, brand voice.
G. Audit memory: immutable/append-only operational events where practical.

Memory must support deletion, retention controls, provenance, and tenant isolation.

## 11. Calls and voice

Recommended production architecture:

Customer phone ↔ Telephony provider ↔ Voice gateway ↔ Hamed Voice Agent ↔ Hamed Orchestrator ↔ Specialist agents/tools

Initial implementation may use Twilio Voice + OpenAI Realtime through Media Streams, but keep a provider abstraction so another telephony vendor can replace Twilio later.

Before call:
- Load customer profile.
- Load verified website findings.
- Load approved offer.
- Load negotiation limits.
- Define call objective.

During call:
- Identify Hamed as an AI assistant.
- Understand the customer.
- Listen naturally.
- Answer questions.
- Handle objections.
- Negotiate only within policy.
- Escalate when needed.
- Offer human handoff.

After call:
- Save transcript/structured summary as allowed.
- Extract objections.
- Record outcome.
- Schedule appropriate follow-up.
- Feed verified result into learning.

Voice must work independently from the owner's personal phone. The owner's device is only an optional control surface. A cloud or always-on host is required for phone calls while the owner's device is offline.

## 12. Channels

Telegram:
- Preserve existing MVP.
- Route through the common orchestrator.

WhatsApp:
- Provider adapter with inbound/outbound messages, templates where required, media, delivery status, and opt-out support.

Voice:
- Same orchestrator and permission layer.

Web Dashboard:
- Admin/operator UI.

All channels use the same business logic; channel-specific code must not contain core business rules.

## 13. Website sales workflow

When Hamed finds a company with an existing website:

DISCOVER → AUDIT → VERIFY ISSUE → ESTIMATE BUSINESS IMPACT → DRAFT OFFER → CONTACT → DISCOVER NEED → NEGOTIATE → CLOSE → DELIVER → MEASURE

Example offer classes:
- Website fixes.
- Website redesign.
- Mobile optimization.
- SEO improvement.
- Conversion optimization.
- WhatsApp/customer-contact integration.
- Content improvements.
- E-commerce upgrades.
- Monthly digital-growth package.

When a company has no website:
- Offer an appropriate starter site, catalog, booking site, or e-commerce store based on actual need.

## 14. Affiliate marketing system

Pipeline:

PROGRAM DISCOVERY → PRODUCT EVALUATION → AUDIENCE FIT → CONTENT/OFFER → DISTRIBUTION → TRACKING → CONVERSION → REVENUE → CUSTOMER FEEDBACK → OPTIMIZATION

Track:
- source
- affiliate program
- product
- commission rate
- effective earnings per conversion
- conversion rate when available
- refund/reversal signals
- traffic source
- content variant
- customer segment
- test status

Do not promote low-quality or unsuitable products solely because the commission is high.

## 15. Experiment engine

Every important commercial hypothesis can become an experiment:

hypothesis → baseline → variant A/B → metric → sample/observation period → result → confidence → decision

Metrics may include:
- reply rate
- qualified lead rate
- conversion rate
- average order value
- gross profit
- margin
- revenue per lead
- affiliate EPC/revenue when available
- retention
- refund/complaint rate
- customer satisfaction

Hamed should prefer evidence from repeated outcomes over anecdotes.

## 16. Negotiation framework

Before negotiation determine:
- target
- minimum acceptable value
- maximum discount
- payment boundaries
- delivery boundaries
- authorized bonuses
- walk-away conditions
- escalation threshold

Preferred order:
1. Understand objection.
2. Clarify interests.
3. Protect value.
4. Trade non-price concessions.
5. Offer structured options.
6. Confirm agreement.
7. Escalate exceptions.

Never fabricate competitor offers, scarcity, deadlines, guarantees, or authority.

## 17. Pricing and finance

Core formulas:

landed_cost = purchase_cost + shipping_cost + known_taxes + known_fees
expected_revenue = unit_sale_price × quantity
expected_gross_profit = expected_revenue - landed_cost
gross_margin_percent = expected_gross_profit / expected_revenue × 100 when expected_revenue > 0

When relevant also calculate:
- customer acquisition cost
- contribution margin
- affiliate earnings
- expected value
- payback period

Unknown values must be labeled "unknown" or "estimated".

## 18. Approval and authority model

Default:
- Research: autonomous.
- Draft messages/offers: autonomous.
- Routine communication: only when explicitly enabled.
- Negotiation: within configured limits.
- Purchase: approval required.
- Payment: approval required.
- Contract: approval required.
- Publishing website: approval required by default.
- Refund above threshold: approval required.
- Account changes: approval required.
- Irreversible actions: approval required.

Approval object:
- action
- counterparty
- item
- quantity
- amount/value
- expected benefit
- profit/margin estimate
- risks
- evidence
- proposed execution steps
- expiry
- current state

Silence is never approval.

## 19. Security

- Environment variables/secret manager for credentials.
- No secrets in Git history.
- Webhook signature validation.
- Rate limiting.
- Idempotency keys.
- Server-side RBAC/authorization.
- Input validation.
- Prompt-injection defenses.
- Secure logging.
- No arbitrary shell/SQL/HTTP execution from model output.
- Tool registry with explicit permissions.
- Tenant isolation.
- Minimal personal data.

## 20. Tool contract

Each tool declares:
- name
- description
- permissions
- input schema
- output schema
- read_only
- reversible
- risk_level
- audit_required

Orchestrator checks policy before every tool execution.

## 21. Dashboard

Provide:
- Executive overview.
- Revenue.
- Profit/margin.
- Sales funnel.
- Leads.
- Customers.
- Conversations.
- Calls.
- Purchasing opportunities.
- Suppliers.
- Affiliate campaigns.
- Website opportunities.
- Learning/strategy leaderboard.
- Experiments.
- Approvals.
- Tasks/workflows.
- Audit events.
- Integration health.

## 22. Autonomous opportunity scanning

Scheduled jobs should scan for:
- New products.
- New suppliers.
- Price changes.
- Affiliate programs.
- Businesses without websites.
- Websites with public, verifiable issues.
- Businesses with weak digital conversion paths.
- New marketing trends.
- Relevant content and case studies.

Jobs must be idempotent and observable.

## 23. Revenue-first operating mode

Default mode before revenue:
- Use free/open-source/local tools wherever practical.
- Disable paid integrations unless explicitly enabled.
- Prefer simulation and testing.
- Track resource consumption.
- Never let the model spend money automatically.

After revenue starts:
- Reinvest a controlled percentage of revenue into compute, AI, telephony, data, and automation.
- Maintain a budget ceiling.
- Require approval for changing budget ceilings.

## 24. Deployment strategy

The application must support:
A. Local Windows server for development/testing.
B. Cloud deployment for 24/7 production.

The local computer can be the initial free host, but Hamed stops when the computer is off.

Cloud deployment must be provider-agnostic. Candidate free tiers can be used for early testing, but production decisions must verify current pricing/limits at deployment time.

The project should include:
- Dockerfile.
- Health endpoint.
- Environment configuration.
- Startup command.
- Basic health checks.
- Restart policy where supported.
- Deployment documentation.

## 25. API configuration

Required environment variables should be optional where features are disabled:

OPENAI_API_KEY=
OPENAI_MODEL=
TELEGRAM_BOT_TOKEN=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_FROM_NUMBER=
PUBLIC_BASE_URL=
DATABASE_URL=
APP_ENV=development
LOG_LEVEL=INFO

Never commit real values.

## 26. Data model

Minimum entities:
- User
- Organization
- Role
- Permission
- Agent
- Customer
- CustomerEvent
- Supplier
- Product
- Offer
- Opportunity
- AffiliateProgram
- AffiliateCampaign
- Quote
- Order
- ApprovalRequest
- Negotiation
- Message
- Call
- Conversation
- Workflow
- Task
- Experiment
- LearningItem
- Strategy
- AuditEvent
- Integration
- CredentialReference
- Website
- WebsiteAudit
- ServiceProposal

## 27. Observability

Record:
- request_id
- session_id
- agent_execution_id
- tool_execution_id
- timestamps
- latency
- errors
- provider/model metadata where appropriate
- estimated API cost where available
- outcome
- approval state

Never log secrets or unnecessary sensitive data.

## 28. Testing

Required tests:
- Pricing calculations.
- Margin calculations.
- Expected-value calculations.
- Authorization.
- Approval gates.
- Negotiation limits.
- Prompt-injection resistance.
- Webhook validation.
- Idempotency.
- Voice adapter contract.
- Telegram flow.
- WhatsApp adapter contract.
- Website audit parsing.
- Learning updates.
- CRM persistence.
- Failure/retry.
- Tool schemas.

Use mocked external services in CI.

## 29. Codex execution protocol

Codex must:
1. Inspect the entire current repository before modifying architecture.
2. Preserve working features.
3. Implement incrementally.
4. Prefer typed models and structured outputs.
5. Keep business logic independent of channels.
6. Keep external provider logic behind adapters.
7. Never fake production success.
8. Never add secrets.
9. Add/adjust tests with meaningful changes.
10. Run tests and startup checks after changes.
11. Keep commits small and descriptive.
12. Update documentation when behavior changes.

## 30. Definition of done

Hamed is complete when:
- It can manage text and voice requests through one orchestrator.
- It can research and verify commercial information.
- It can search and compare products/suppliers.
- It can calculate economics.
- It can find sales/service opportunities.
- It can audit websites.
- It can sell website/store/marketing services.
- It can support affiliate workflows.
- It can negotiate within authority.
- It can remember relevant customer/business context.
- It learns from sources and outcomes.
- It can conduct permitted voice calls through a pluggable telephony adapter.
- It can operate independently of the owner's phone.
- It blocks unauthorized consequential actions.
- It keeps an audit trail.
- It has tests for critical safety and business logic.
- It can run locally and is portable to cloud infrastructure.

## 31. Canonical behavior examples

### Example A — product opportunity
User: "Find me a product I can buy cheaply and resell with a good margin."

Hamed:
- Researches candidates.
- Finds suppliers.
- Normalizes costs.
- Estimates revenue.
- Calculates profit and margin.
- Ranks opportunities.
- Explains assumptions and risks.
- Requests approval only when an actual purchase is ready.

### Example B — existing website
User: "Find customers who need website improvements."

Hamed:
- Finds suitable businesses using permitted public information.
- Crawls permitted public pages.
- Detects evidence-backed issues.
- Builds a personalized outreach message.
- Contacts only through enabled/authorized channels.
- Handles objections.
- Sells improvement work if the customer needs it.
- Records the result.

### Example C — no website
Hamed finds a seller without a website:
- Understands the business.
- Recommends the appropriate website/store.
- Prepares a proposal.
- Negotiates within limits.
- Obtains approval before publishing.

### Example D — affiliate opportunity
Hamed finds a quality product with a legitimate affiliate program:
- Checks audience fit and evidence.
- Estimates economics.
- Creates a content/test plan.
- Discloses affiliate relationship where required.
- Tracks performance.
- Keeps or drops the program based on measured results.

### Example E — voice sales
User enables phone outreach to an authorized list:
- Hamed loads each customer brief.
- Calls through configured telephony provider.
- Identifies itself as AI.
- Discovers needs.
- Presents an appropriate offer.
- Negotiates within limits.
- Escalates exceptions.
- Logs outcome and learns from verified results.

## 32. Final mission statement for Codex

Build Hamed AI as a continuously improving commercial intelligence and execution system. Its job is to discover opportunities, understand people and businesses, create genuine value, sell appropriate products and services, negotiate professionally, generate revenue, and learn from verified evidence. It must be autonomous in thinking and permitted execution, but never autonomous in unauthorized money movement or binding commitments.

This document is the master product and engineering specification. When implementation details conflict with it, preserve security, accuracy, customer trust, server-side authorization, and verified outcomes first.