"""Extensible registry of Hamed specialist agents."""
from dataclasses import dataclass

@dataclass(frozen=True)
class AgentProfile:
    id: str
    name: str
    domain: str
    goal: str
    risk: str = "low"

AGENTS = [
    ("chief", "Chief Agent", "management", "coordinate the whole task"),
    ("planner", "Planner Agent", "reasoning", "turn goals into executable plans"),
    ("decision", "Decision Agent", "reasoning", "compare options and recommend decisions"),
    ("reasoning", "Reasoning Agent", "reasoning", "deep logical analysis"),
    ("critic", "Critic Agent", "quality", "find flaws and counterarguments"),
    ("reviewer", "Reviewer Agent", "quality", "review deliverables before release"),
    ("risk", "Risk Analyst", "risk", "identify operational and commercial risks"),
    ("research-coordinator", "Research Coordinator", "research", "coordinate research tasks"),
    ("business", "Business Strategist", "business", "design business models and strategies"),
    ("finance", "Financial Analyst", "finance", "analyze costs, margins and scenarios"),
    ("pricing", "Pricing Agent", "sales", "build pricing and packaging strategies"),
    ("accounting", "Accounting Assistant", "finance", "organize accounting information"),
    ("investment", "Investment Research", "finance", "research investment opportunities"),
    ("market", "Market Research Agent", "research", "research markets and demand"),
    ("competitor", "Competitor Analysis Agent", "research", "compare competitors"),
    ("business-model", "Business Model Agent", "business", "design viable business models"),
    ("operations", "Operations Agent", "operations", "improve operating workflows"),
    ("procurement", "Procurement Agent", "operations", "research purchasing and suppliers"),
    ("sales", "Sales Agent", "sales", "design ethical sales conversations"),
    ("lead-generation", "Lead Generation Agent", "sales", "find qualified public leads using permitted sources"),
    ("crm", "CRM Agent", "sales", "organize leads and customer pipelines"),
    ("negotiation", "Negotiation Agent", "sales", "prepare negotiation strategies"),
    ("customer-success", "Customer Success Agent", "customer", "increase retention and satisfaction"),
    ("advertising", "Advertising Agent", "marketing", "create and optimize campaigns"),
    ("marketing", "Marketing Strategy Agent", "marketing", "build marketing strategies"),
    ("seo", "SEO Agent", "marketing", "improve organic search visibility"),
    ("conversion", "Conversion Optimization Agent", "marketing", "improve conversion funnels"),
    ("ecommerce", "E-commerce Agent", "commerce", "design and optimize online stores"),
    ("customer-psychology", "Customer Psychology Agent", "customer", "understand customer needs and communication patterns without diagnosis or manipulation"),
    ("buyer-intent", "Buyer Intent Agent", "sales", "identify stated and observable buying intent"),
    ("communication", "Customer Communication Agent", "customer", "write natural customer-facing communication"),
    ("objections", "Objection Handling Agent", "sales", "answer objections honestly and helpfully"),
    ("trust", "Trust & Retention Agent", "customer", "build trust and long-term relationships"),
    ("service-quality", "Service Quality Agent", "customer", "improve service quality"),
    ("psychology-research", "Psychology Research Agent", "learning", "research psychology from credible public sources"),
    ("sales-science", "Sales Science Research Agent", "learning", "research evidence-based sales science"),
    ("service-research", "Customer Service Research Agent", "learning", "research customer service methods"),
    ("strategy-research", "Business Strategy Research Agent", "learning", "research business strategy"),
    ("continuous-learning", "Continuous Learning Agent", "learning", "evaluate new knowledge before adding it to Hamed memory"),
    ("software-architect", "Software Architect", "engineering", "design robust software architecture"),
    ("python", "Python Developer", "engineering", "write and debug Python"),
    ("javascript", "JavaScript Developer", "engineering", "write and debug JavaScript"),
    ("backend", "Backend Developer", "engineering", "build backend services"),
    ("frontend", "Frontend Developer", "engineering", "build frontend interfaces"),
    ("mobile", "Mobile Developer", "engineering", "design mobile applications"),
    ("database", "Database Engineer", "engineering", "design and optimize databases"),
    ("api", "API Engineer", "engineering", "design integrations and APIs"),
    ("devops", "DevOps Agent", "engineering", "build reliable deployment workflows"),
    ("docker", "Docker Agent", "engineering", "containerize and troubleshoot applications"),
    ("github", "GitHub Agent", "engineering", "manage repositories, branches and CI workflows"),
    ("qa", "QA Agent", "quality", "test software and detect regressions"),
    ("security", "Security Review Agent", "security", "identify security weaknesses safely"),
    ("web-builder", "Web Builder", "web", "build complete websites"),
    ("uiux", "UI/UX Designer", "design", "design usable interfaces"),
    ("landing", "Landing Page Agent", "marketing", "build conversion-focused landing pages"),
    ("performance", "Web Performance Agent", "web", "improve performance and reliability"),
    ("technical-seo", "Technical SEO Agent", "marketing", "audit technical SEO"),
    ("accessibility", "Accessibility Agent", "design", "improve accessibility"),
    ("copywriter", "Copywriter", "content", "write persuasive truthful copy"),
    ("content", "Content Strategist", "content", "plan content systems"),
    ("brand", "Brand Strategist", "branding", "develop brand positioning"),
    ("creative", "Creative Director", "creative", "direct creative concepts"),
    ("social", "Social Media Agent", "marketing", "plan platform-appropriate social content"),
    ("video-script", "Video Script Agent", "content", "write video scripts"),
    ("pdf", "PDF Agent", "documents", "analyze and create PDF workflows"),
    ("excel", "Excel/Data Agent", "data", "analyze spreadsheets"),
    ("documents", "Document Agent", "documents", "process business documents"),
    ("data", "Data Analyst", "data", "analyze structured data"),
    ("reports", "Report Generator", "documents", "create professional reports"),
    ("manufacturing", "Manufacturing Agent", "industry", "analyze manufacturing workflows"),
    ("supply-chain", "Supply Chain Agent", "industry", "optimize supply chains"),
    ("food", "Food Industry Agent", "industry", "support food-industry business analysis"),
    ("cosmetics", "Cosmetics Agent", "industry", "support cosmetics business analysis"),
    ("packaging", "Packaging Agent", "industry", "support packaging projects"),
    ("real-estate", "Real Estate Agent", "industry", "analyze real-estate opportunities"),
    ("construction", "Construction Agent", "industry", "support construction planning"),
    ("logistics", "Logistics Agent", "industry", "support logistics planning"),
    ("education", "Education Agent", "industry", "support educational workflows"),
    ("hospitality", "Hospitality Agent", "industry", "support hospitality operations"),
    ("linkedin-prospecting", "LinkedIn Prospecting Agent", "client-research", "research public professional leads and opportunities without bypassing access controls"),
    ("meta-prospecting", "Facebook & Instagram Prospecting Agent", "client-research", "research public business profiles and opportunities using permitted access"),
    ("short-video-prospecting", "TikTok & YouTube Prospecting Agent", "client-research", "identify public creator/business opportunities without spam or mass messaging"),
    ("x-prospecting", "X Prospecting Agent", "client-research", "research public conversations and business opportunities while respecting platform rules"),
    ("web-prospecting", "Web & Social Opportunity Agent", "client-research", "combine public web and social signals into qualified lead research"),
]

AGENT_REGISTRY = {a[0]: AgentProfile(*a) for a in AGENTS}
assert len(AGENT_REGISTRY) >= 80, "Hamed must ship with at least 80 specialist profiles"

# Five dedicated client-research agents. They research public, permitted information;
# they never mass-message, spam, bypass controls, or collect sensitive personal data.
CLIENT_RESEARCH_AGENTS = (
    "linkedin-prospecting",
    "meta-prospecting",
    "short-video-prospecting",
    "x-prospecting",
    "web-prospecting",
)

LEARNING_COUNCIL = (
    "psychology-research",
    "sales-science",
    "service-research",
    "strategy-research",
    "continuous-learning",
)
