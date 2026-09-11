# HAMED AGI SPECIFICATION

## 1. Vision
Hamed is an autonomous commercial intelligence system built on top of a general-purpose model, a council of specialist agents, persistent memory, tools, planning, self-critique, learning, and controlled execution.

The objective is not to train a foundation model from scratch. The objective is to create an AGI-like cognitive operating layer that can understand broad goals, decompose them, recruit the right specialists, use tools, evaluate evidence, execute permitted work, measure outcomes, and improve future decisions.

## 2. Core cognitive loop
Every non-trivial mission follows:

1. Understand the user's goal and constraints.
2. Load relevant memory and prior outcomes.
3. Define measurable success criteria.
4. Generate multiple candidate approaches.
5. Select specialist agents and tools.
6. Build an executable plan.
7. Deliberate with the brain council when useful.
8. Critique the plan and search for failure modes.
9. Apply risk and approval gates.
10. Execute permitted steps.
11. Verify outputs and real-world results.
12. Record what worked, failed, and why.
13. Convert reliable lessons into reviewed long-term knowledge.
14. Re-plan when evidence contradicts assumptions.

## 3. Cognitive layers

### A. Identity and objective layer
Maintains owner identity, business objectives, priorities, constraints, budget limits, risk tolerance, and operating policies.

### B. World model
Stores structured knowledge about customers, markets, products, suppliers, competitors, offers, projects, experiments, prices, and observed outcomes.

### C. Memory
Use short-term conversation state plus durable business memory. Every important memory item should have source, timestamp, confidence, scope, and update history. Unverified claims must not silently become trusted facts.

### D. Planner
Turns a goal into ordered or parallel steps. It may revise the plan after tool results or failed steps.

### E. Brain council
Uses multiple model/provider perspectives for difficult decisions. The council should produce independent reasoning summaries, disagreements, confidence, alternatives, and a final synthesis. Provider failure must degrade gracefully to another configured provider.

### F. Specialist agent network
Hamed already contains a large specialist registry and dedicated commercial agents. Agents remain focused workers; the cognitive runtime decides when and why to use them.

### G. Tool layer
Tools include web research, CRM, documents/data, communication, software development, and future external integrations. Tools must declare capabilities, permissions, cost, and risk.

### H. Judge / critic
Before consequential execution, evaluate factual support, objective alignment, completeness, uncertainty, expected value, downside risk, and policy compliance.

### I. Execution layer
Executes only actions permitted by policy. External side effects must be observable and auditable.

### J. Learning layer
Learning is evidence-driven. Hamed records hypotheses, experiments, results, lessons, and confidence. Long-term knowledge is promoted only after validation according to source quality and outcome evidence.

## 4. Autonomy levels

- L0: Answer only.
- L1: Research and propose.
- L2: Plan and prepare artifacts.
- L3: Execute reversible low-risk actions automatically.
- L4: Execute bounded business workflows with explicit policy authorization.
- L5: High-impact actions require owner approval immediately before execution.

Financial transfers, purchases, legally binding commitments, credential/security changes, irreversible deletion, mass outreach, or other high-impact actions must never bypass their configured approval gate.

## 5. Opportunity engine
Hamed continuously looks for legitimate commercial opportunities across Arab markets and broader online markets. Candidate opportunities are scored using:

- problem severity
- evidence of demand
- customer accessibility
- competition
- expected revenue
- gross margin potential
- capital required
- time to first revenue
- execution complexity
- legal/platform constraints
- downside risk
- confidence in evidence

The engine should prefer opportunities that can be tested cheaply before significant capital is committed.

## 6. Universal customer workflow
For a qualified public business lead:

Research -> identify problem -> verify evidence -> design offer -> estimate value -> personalize communication -> negotiate ethically -> deliver service -> measure outcome -> request retention/upsell opportunity.

No spam, mass unsolicited messaging, access-control bypass, scraping of sensitive personal data, deceptive identity, or fabricated claims.

## 7. Self-improvement
Hamed should improve the system without silently rewriting production behavior. Proposed changes become improvement candidates with:

- reason for change
- evidence
- expected benefit
- regression risk
- tests required
- rollback plan
- approval status

Code-changing agents may prepare patches and tests; deployment of consequential changes remains gated.

## 8. Provider architecture
The cognitive layer must be provider-agnostic. A configured provider may be OpenAI, Anthropic/Claude, Gemini, DeepSeek, Kimi, or another compatible backend. Routing should consider task type, quality, latency, availability, and cost. Secrets remain in environment/configuration and never in source control.

## 9. Failure recovery
When a plan step fails, Hamed should classify the failure as transient, tool/input, reasoning, permission, provider, or external-world failure. It may retry bounded transient failures, select another agent/tool, or re-plan. Repeated failure must stop the affected branch and report the reason rather than loop indefinitely.

## 10. Observability
Each mission should have a trace containing:

- mission ID
- goal
- selected agents
- selected tools
- plan versions
- decisions and confidence
- approvals
- tool calls and outcomes
- execution results
- errors
- final outcome
- lessons learned

Sensitive credentials and unnecessary personal data must never enter traces.

## 11. API/runtime contract
The AGI runtime should expose conceptual operations for:

- create_goal
- load_context
- build_plan
- deliberate
- critique
- request_approval
- execute
- verify
- learn
- retrieve_memory
- replan
- summarize_mission

The current `app/agi/cognitive_runtime.py` implements the foundation for goal, planning, deliberation, critique, gated execution, and learning. Future integrations should connect it to `HamedOrchestrator`, the existing BrainCouncil, Repository/database memory, and ToolRegistry rather than duplicating those systems.

## 12. Acceptance criteria
The AGI foundation is considered integrated when all are true:

1. A natural-language mission can become a structured goal.
2. Relevant memory is loaded before planning.
3. Hamed can select multiple specialist agents for one mission.
4. A plan can contain dependencies, parallel branches, risk, and approval requirements.
5. Brain-council deliberation can be invoked for difficult decisions.
6. A critic can block weak or unsafe plans.
7. Low-risk reversible tasks can execute through the existing orchestrator.
8. High-impact tasks stop at an approval gate.
9. Failed steps can trigger bounded recovery/replanning.
10. Results are verified rather than assumed successful.
11. Outcomes become structured learning records.
12. The complete mission is auditable.
13. Existing Hamed tests continue to pass.
14. The AGI layer can operate with one configured model and gracefully support multiple providers later.

## 13. Build order
Phase 1: cognitive runtime foundation. DONE on `feat/agi-foundation`.

Phase 2: integrate runtime with HamedOrchestrator, Repository, BrainCouncil, and ToolRegistry.

Phase 3: add structured mission state, memory retrieval, plan persistence, and replanning.

Phase 4: add verification/evaluation and outcome-based learning promotion.

Phase 5: add autonomous opportunity discovery loops with strict rate, cost, and communication controls.

Phase 6: connect Telegram/WhatsApp reporting and owner approval UX.

Phase 7: run full regression, security, reliability, and cost tests before production deployment.

## 14. Definition of success
Success is not measured by how autonomous Hamed sounds. It is measured by whether Hamed reliably turns broad goals into useful, evidence-backed actions, produces measurable business outcomes, learns from those outcomes, and remains controllable and auditable while doing so.
