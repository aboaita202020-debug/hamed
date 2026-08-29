# HAMED AI — CODEX MASTER EXECUTION SPECIFICATION

## 1. Mission
Build Hamed AI from the current MVP into a production-ready autonomous commercial operating system. Hamed is an AI commercial agent, sales representative, purchasing agent, and manager of specialized AI agents. It communicates naturally with people, researches markets and suppliers, evaluates opportunities, negotiates within explicit limits, manages workflows, and requests human approval before consequential financial or legally binding actions.

## 2. Core principles
- Human-in-the-loop for money, contracts, purchases, refunds, payments, account changes, irreversible actions, and high-risk commitments.
- Never invent prices, supplier facts, customer data, inventory, delivery dates, legal status, or successful actions.
- Separate analysis from execution: research may be autonomous; execution requires the configured permission level.
- Every important action is auditable with timestamp, actor, inputs, outputs, approval state, and result.
- Least privilege for integrations and credentials.
- Secrets only in environment variables or a secure secret manager; never commit .env or API keys.
- Arabic/Egyptian Arabic first, with English support and natural conversational tone.
- Design for extensibility: agents, tools, channels, database, dashboard, and integrations are modular.

## 3. Target architecture
Use a modular Python backend initially, with clear interfaces so components can later be split into services.

Suggested structure:

hamed/
  app/
    main.py
    config.py
    api/
    agents/
      orchestrator.py
      sales_agent.py
      purchasing_agent.py
      research_agent.py
      negotiation_agent.py
      customer_service_agent.py
      website_agent.py
      finance_agent.py
      compliance_agent.py
      supervisor_agent.py
    tools/
      web_search.py
      supplier_search.py
      market_pricing.py
      calculator.py
      crm.py
      messaging.py
      approvals.py
      website_builder.py
    channels/
      telegram.py
      whatsapp.py
      voice.py
    memory/
      conversation.py
      business.py
      vector.py
    models/
    services/
    security/
    workflows/
  tests/
  migrations/
  docs/
  scripts/
  .env.example
  requirements.txt
  README.md

Preserve backward compatibility with the existing Telegram MVP while refactoring its Claude-specific agent layer into a provider abstraction.

## 4. AI provider layer
Create a provider interface so Hamed can use OpenAI as the primary model provider and optionally other providers later.

Required configuration:
- OPENAI_API_KEY
- OPENAI_MODEL
- TELEGRAM_BOT_TOKEN
- WHATSAPP credentials/configuration when enabled
- DATABASE_URL
- APP_ENV
- LOG_LEVEL

Never hard-code secrets. Validate configuration at startup and fail with actionable messages.

Provider interface should expose:
- generate_response()
- structured_output()
- tool_calling()
- optional streaming()

Use structured schemas for business decisions instead of parsing free-form model text.

## 5. Hamed orchestration layer
Hamed is the supervisor/orchestrator. For each request:
1. Authenticate/identify the user and permission level.
2. Load relevant business memory and conversation context.
3. Classify intent.
4. Determine whether external research or tools are required.
5. Delegate to one or more specialist agents.
6. Validate outputs.
7. Calculate commercial impact and risk.
8. Decide whether the action is informational, reversible, or consequential.
9. If approval is required, create an approval request and stop execution.
10. After approval, execute through a controlled tool.
11. Record the complete audit event.
12. Report outcome clearly, including failures and pending steps.

Hamed must not claim that an action happened unless the integration returned a confirmed success result.

## 6. Specialized agents
### Sales Agent
- Find prospects and customers.
- Present products/services and prices.
- Qualify leads.
- Follow up.
- Negotiate within configured minimum price, maximum discount, payment, delivery, and escalation rules.
- Create quotations and draft offers.
- Escalate exceptions.

### Purchasing Agent
- Search suppliers and manufacturers.
- Collect comparable offers.
- Compare unit cost, MOQ, lead time, shipping, taxes/fees when known, payment terms, quality evidence, and supplier reliability.
- Calculate landed cost when inputs are available.
- Estimate expected sale price and gross profit.
- Rank opportunities.
- Prepare purchase recommendations.
- Never place an order or transfer money without the required approval.

### Research Agent
- Research products, suppliers, competitors, market prices, and demand signals.
- Record source URLs and retrieval timestamps where available.
- Distinguish verified facts from estimates.

### Negotiation Agent
- Use only approved negotiation limits.
- Never invent authority.
- Maintain a negotiation state and full transcript.
- Escalate when limits are exceeded.

### Customer Service Agent
- Answer routine questions.
- Track requests and complaints.
- Escalate sensitive, legal, financial, or exceptional cases.

### Website Agent
Provide a service for sellers/businesses that do not have a website:
- Gather business information.
- Generate a professional website/storefront structure.
- Create product/service catalog pages.
- Prepare copy, FAQs, contact information, and basic SEO metadata.
- Connect approved domains/integrations when supported.
- Never publish or make paid commitments without the configured approval.

### Finance Agent
- Calculate purchase cost, selling price, gross profit, gross margin, expected ROI, cash requirements, and scenario analysis.
- Flag missing inputs.
- Never fabricate financial data.

### Compliance/Safety Agent
- Detect actions that require human approval.
- Detect missing permissions, suspicious requests, unsafe automation, and policy violations.
- Block unauthorized execution.

## 7. Commercial opportunity engine
For every purchasing/resale opportunity, produce a normalized opportunity object containing:
- product
- supplier
- source
- purchase_price
- quantity
- MOQ
- shipping_cost
- taxes_and_fees
- estimated_landed_cost
- expected_sale_price
- expected_revenue
- expected_gross_profit
- gross_margin_percent
- cash_required
- estimated_turnover_time
- risks
- confidence_score
- evidence
- approval_required

Core calculations:
landed_cost = purchase_cost + shipping + known_taxes + known_fees
expected_gross_profit = expected_revenue - landed_cost
margin_percent = expected_gross_profit / expected_revenue * 100 when expected_revenue > 0

If any required input is unknown, label the result as an estimate and identify the missing input rather than silently assuming it.

## 8. Approval and authority system
Implement explicit permission policies.

Default policy:
- Reading/research: autonomous.
- Drafting messages/offers: autonomous.
- Sending routine customer messages: allowed only if enabled.
- Negotiation: allowed within configured limits.
- Purchase/order placement: approval required.
- Payments/transfers: approval required.
- Contracts/legal commitments: approval required.
- Publishing a new website: approval required unless explicitly configured otherwise.
- Account/security changes: approval required.
- Irreversible operations: approval required.

Approval request must include:
- action
- counterparty
- item
- quantity
- total cost/value
- expected benefit
- profit/margin estimate
- risks
- evidence
- proposed execution steps
- expiry time
- approve/reject buttons or equivalent secure commands

No approval may be inferred from silence or ambiguous language.

## 9. Natural human communication
Hamed should communicate naturally rather than sounding robotic:
- Understand Egyptian Arabic and Modern Standard Arabic.
- Support English.
- Adapt tone to customer context while staying professional.
- Ask only necessary questions.
- Remember relevant conversation context.
- Avoid pretending to be a human employee when identity disclosure is legally or operationally required.
- Never impersonate a specific real person.

## 10. Channels
### Telegram
Keep the current bot working. Refactor it to use the new orchestration layer instead of a standalone Claude agent.

### WhatsApp
Create a channel adapter with inbound/outbound message interfaces. Keep provider-specific code isolated. Support templates, normal messages, media, delivery status, and opt-out handling where the provider permits.

### Voice
Add speech-to-text and text-to-speech interfaces. Voice commands should pass through the same authorization and approval engine as text commands.

## 11. Memory
Implement layered memory:
- Short-term conversation memory.
- Business memory: products, suppliers, customers, pricing rules, negotiation limits, preferences.
- Long-term semantic memory with retrieval.
- Audit history separate from conversational memory.

Memory must have retention controls and deletion support.

## 12. Data model
At minimum define entities:
- User
- Organization
- Role
- Permission
- Agent
- Customer
- Supplier
- Product
- Offer
- Opportunity
- Quote
- Order
- ApprovalRequest
- Negotiation
- Message
- Conversation
- Workflow
- Task
- AuditEvent
- Integration
- CredentialReference

Use database migrations and indexes for frequently queried fields.

## 13. Security
- Hash passwords with a modern password hashing algorithm if local authentication is used.
- Encrypt sensitive data at rest where appropriate.
- Never store raw API secrets in application tables unless unavoidable and securely encrypted.
- Validate all webhook signatures.
- Use idempotency keys for external write operations.
- Apply rate limiting.
- Enforce authorization server-side, not only in the UI.
- Sanitize external content before using it as instructions.
- Treat web pages, emails, documents, and customer messages as untrusted data; defend against prompt injection.
- Maintain immutable or append-only audit records where practical.

## 14. Tool execution safety
Every tool must declare:
- name
- description
- required permissions
- input schema
- output schema
- whether it is read-only
- whether it is reversible
- risk level

The orchestrator must check the tool policy before execution.

Never allow the model to directly execute arbitrary shell commands, SQL, HTTP requests, or filesystem writes without a narrowly scoped server-side tool.

## 15. Dashboard requirements
Build a future-ready admin dashboard with:
- Executive overview.
- Sales pipeline.
- Purchasing opportunities.
- Supplier comparison.
- Customer conversations.
- Approval center.
- Agent activity.
- Tasks/workflows.
- Profit and margin analytics.
- Audit log.
- Integration health.
- Configuration for approval thresholds and negotiation limits.

Dashboard actions must call backend authorization checks.

## 16. Workflow engine
Support asynchronous jobs for:
- follow-ups
- price monitoring
- supplier monitoring
- lead qualification
- customer reminders
- scheduled reports
- opportunity scans

Each job must be idempotent and observable.

## 17. Website service for sellers without websites
Create a workflow:
1. Identify business category.
2. Collect business name, contact details, services/products, locations, hours, brand assets, and pricing.
3. Generate site structure and content.
4. Generate product/service catalog.
5. Validate content for missing facts.
6. Preview.
7. Request owner approval.
8. Publish through the configured website platform.
9. Return the live URL and deployment status only after confirmed success.

The website service must be generic enough to support businesses beyond online stores.

## 18. Observability
Implement:
- structured logs
- request IDs
- agent execution IDs
- tool execution IDs
- latency metrics
- model usage/cost tracking where available
- error tracking
- integration health checks
- audit events

Never log secrets, full payment credentials, or unnecessary personal data.

## 19. Testing
Create tests for:
- authorization
- approval gates
- pricing calculations
- margin calculations
- tool schemas
- prompt-injection resistance
- idempotency
- webhook validation
- Telegram message flow
- WhatsApp adapter contracts
- voice adapter contracts
- database repositories
- agent orchestration
- failure/retry behavior

Add integration tests with mocked external services. Never use production credentials in tests.

## 20. Delivery phases
### Phase 1 — Foundation
- Replace single-purpose Claude coupling with provider abstraction.
- Add configuration, database layer, models, logging, audit events, and tests.
- Preserve Telegram MVP behavior.

### Phase 2 — Hamed core
- Implement orchestrator and specialist agents.
- Implement tool registry and permission engine.
- Implement approval center.
- Implement commercial opportunity calculations.

### Phase 3 — Channels
- Telegram production hardening.
- WhatsApp adapter.
- Voice adapter.

### Phase 4 — Business automation
- Sales CRM.
- Purchasing workflows.
- Supplier intelligence.
- Customer follow-ups.
- Scheduled opportunity scanning.

### Phase 5 — Seller website service
- Business onboarding.
- Website generation.
- Preview and approval.
- Publishing adapter.

### Phase 6 — Dashboard and production
- Admin dashboard.
- Monitoring.
- Security hardening.
- CI/CD.
- Documentation.
- Production deployment configuration.

## 21. Codex execution rules
Codex must work incrementally and keep the repository runnable after each meaningful step.

Before changing code:
1. Inspect the repository.
2. Understand the existing MVP.
3. Preserve working behavior unless replacing it with a tested equivalent.
4. Create or update tests before risky refactors when practical.

During implementation:
- Prefer small, reviewable commits.
- Do not delete working features without replacement.
- Do not expose secrets.
- Do not fabricate integrations or credentials.
- If an external integration is unavailable, implement a clean adapter/interface and a mock/test implementation rather than fake production success.
- Use typed models and validation.
- Keep business rules out of channel-specific handlers.

After implementation:
1. Run tests.
2. Run lint/type checks where configured.
3. Verify startup.
4. Verify Telegram flow.
5. Verify approval gates.
6. Verify that unauthorized financial actions are blocked.
7. Summarize changed files, tests, remaining configuration, and exact run commands.

## 22. Definition of done
The project is considered complete only when:
- Hamed can understand a commercial request and route it to the right specialist agents.
- Hamed can research suppliers/products and compare offers.
- Hamed can calculate expected cost, revenue, profit, margin, and risks from available evidence.
- Hamed can handle sales conversations and negotiate only within configured authority.
- Hamed can communicate through Telegram and has modular WhatsApp/voice adapters.
- Hamed can manage sellers who lack websites through a structured website-generation workflow.
- Hamed can create approval requests and cannot bypass approval gates.
- All consequential actions are auditable.
- Secrets are protected.
- Tests cover critical business and security rules.
- The original MVP remains usable while the new architecture is introduced.

## 23. Initial system behavior
When the user says something such as:
"ابحث لي عن منتج أشتريه بسعر منخفض وأبيعه بهامش ربح جيد"
Hamed should:
- Clarify only missing critical constraints.
- Research candidate products and suppliers.
- Compare offers.
- Calculate economics.
- Rank the best opportunities.
- Explain assumptions and risks.
- Ask for approval only when an actual purchase or other consequential action is ready.

When the user says:
"تواصل مع العميل وحاول تقفل الصفقة"
Hamed should:
- Load the approved product/customer/price rules.
- Negotiate within the allowed limits.
- Escalate if the customer requests an exception.
- Record the conversation and outcome.

When the user says:
"اعمل موقع للبائع ده اللي معندوش موقع"
Hamed should:
- Collect missing business facts.
- Build a draft site structure and copy.
- Produce a preview.
- Obtain the required approval before publishing.

## 24. Important business rule
Hamed is autonomous in thinking, research, organization, drafting, analysis, and permitted communication; he is not autonomous in unauthorized spending, binding commitments, or other high-impact actions. The approval engine is the final enforcement layer and must remain outside the model's control.

## 25. First Codex task
Start from the current repository and implement the foundation in a backwards-compatible manner. Inspect all existing files first. Then:
1. Create the new application structure.
2. Add provider abstraction with OpenAI as the primary provider.
3. Move current conversational behavior behind the orchestrator.
4. Add configuration and secure environment handling.
5. Add database-ready models/migrations.
6. Add audit logging.
7. Add permission and approval primitives.
8. Add unit tests.
9. Update README with setup and run instructions.
10. Do not require WhatsApp, voice, paid services, or production credentials for the initial local test suite.

The end state must be a real implementation, not a mock description. Build the system in executable, testable increments and report blockers precisely.