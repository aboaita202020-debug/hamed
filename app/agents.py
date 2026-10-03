from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .provider_router import provider_router


@dataclass
class AgentResult:
    agent: str
    status: str
    output: dict[str, Any]

@dataclass(frozen=True)
class AgentSpec:
    name: str
    role: str
    department: str
    leader: bool = False
    capabilities: tuple[str, ...] = ()

class SalesAgent:
    """Backward-compatible sales facade."""
    def run(self, payload: dict[str, Any]) -> AgentResult:
        return AgentResult("sales", "ok", {"objective": str(payload.get("objective", "")), "department": "Sales & Revenue"})


class Agent:
    def __init__(self, spec: AgentSpec):
        self.spec = spec
        self.name = spec.name
        self.role = spec.role
        self.department = spec.department
    def run(self, payload: dict[str, Any]) -> AgentResult:
        objective = str(payload.get("objective", ""))
        context = payload.get("context") or {}
        prompt = (
            "You are a specialized ORVIA AGI worker.\n"
            f"Agent: {self.name}\nRole: {self.role}\nDepartment: {self.department}\n"
            f"Capabilities: {list(self.spec.capabilities)}\n"
            f"Objective: {objective}\n"
            f"Prior agent context keys: {sorted(context.keys())}\n"
            "Perform your assigned analysis, return concise evidence-based findings, "
            "next action, risks, and any information another agent should receive. "
            "Do not claim external actions you did not perform."
        )
        provider = provider_router.select()
        text = provider.generate(prompt)
        state = provider.state()
        return AgentResult(self.name, "ok" if state.mode == "connected" else "fallback", {
            "role": self.role, "department": self.department,
            "leader": self.spec.leader, "capabilities": list(self.spec.capabilities),
            "received_context_keys": sorted(context.keys()),
            "provider": state.name, "model": state.model,
            "connected": state.mode == "connected", "analysis": text,
        })

class SalesAgent:
    """Backward-compatible sales facade used by legacy callers/tests."""
    def run(self, payload: dict[str, Any]) -> AgentResult:
        return AgentResult("sales", "ok", {"objective": str(payload.get("objective", "")), "department": "Sales & Revenue"})

_DEPARTMENTS = [
("Research & Intelligence",202,["research","trends","sources"]),
("E-commerce & Product",202,["stores","UX","conversion"]),
("Cybersecurity & Sentinel",252,["security","threat_intel","authorized_assessment"]),
("Marketing & Growth",202,["content","SEO","growth"]),
("Sales & Revenue",202,["leads","offers","revenue"]),
("Negotiation & Customer Psychology",152,["negotiation","behavior","messaging"]),
("Websites & Software",152,["web","software","automation"]),
("Analytics & Decision",152,["metrics","risk","decisions"]),
("B2B & Business Opportunities",152,["B2B","partnerships","opportunities"]),
("Learning & Knowledge",152,["learning","knowledge","feedback"]),
("Automation & Operations",100,["workflow","operations","routing"]),
("Reporting, CRM & Kids Media Intelligence",100,["CRM","reporting","kids_trends","youtube_analytics"]),
]
_ROLE_BANK = {
"Research & Intelligence":["market researcher","trend researcher","source verifier","competitor researcher","public-data analyst"],
"E-commerce & Product":["store analyst","UX analyst","conversion analyst","product researcher","catalog analyst"],
"Cybersecurity & Sentinel":["web security analyst","API security analyst","threat intelligence analyst","vulnerability analyst","verification analyst"],
"Marketing & Growth":["content strategist","SEO analyst","growth analyst","campaign analyst","creative strategist","UGC researcher","UGC scriptwriter","UGC creative strategist","UGC performance analyst"],
"Sales & Revenue":["lead researcher","sales analyst","offer strategist","revenue analyst","pipeline analyst"],
"Negotiation & Customer Psychology":["negotiation analyst","customer psychology analyst","objection analyst","messaging analyst","buyer journey analyst"],
"Websites & Software":["web architect","software analyst","automation analyst","QA analyst","integration analyst"],
"Analytics & Decision":["data analyst","experiment analyst","risk analyst","decision analyst","KPI analyst"],
"B2B & Business Opportunities":["B2B researcher","partnership analyst","market matcher","opportunity researcher","business model analyst"],
"Learning & Knowledge":["knowledge researcher","learning analyst","feedback analyst","knowledge curator","self-improvement analyst"],
"Automation & Operations":["workflow planner","operations analyst","task router","process analyst","reliability analyst"],
"Reporting, CRM & Kids Media Intelligence":["CRM analyst","reporting analyst","kids media trend analyst","YouTube analytics analyst","content performance analyst"],
}
_specs=[]
for dept,count,caps in _DEPARTMENTS:
    key=dept.lower().replace(" & ","_").replace(" ","_")
    _specs.append(AgentSpec("leader_"+key,dept.lower()+" lead",dept,True,tuple(caps)))
    roles=_ROLE_BANK[dept]
    for i in range(count-1):
        _specs.append(AgentSpec(f"{key}_{i+1:02d}",roles[i%len(roles)],dept,False,tuple(caps)))

_core=[
("research","public evidence research","Research & Intelligence"),
("sales","lead qualification and sales","Sales & Revenue"),
("marketing","growth and campaigns","Marketing & Growth"),
("negotiation","non-binding negotiation","Negotiation & Customer Psychology"),
("customer_psychology","customer behavior analysis","Negotiation & Customer Psychology"),
("affiliate","affiliate opportunity analysis","B2B & Business Opportunities"),
("crm","customer relationship intelligence","Reporting, CRM & Kids Media Intelligence"),
("website_factory","website and store planning","Websites & Software"),
("analytics","metrics and experiments","Analytics & Decision"),
("b2b","business matching","B2B & Business Opportunities"),
("reporting","operational reporting","Reporting, CRM & Kids Media Intelligence"),
("decision","risk-aware decisions","Analytics & Decision"),
("audit","evidence and audit trail","Analytics & Decision"),
("learning","feedback and self-improvement","Learning & Knowledge"),
("revenue","revenue opportunity analysis","Sales & Revenue"),
("sentinel","e-commerce security scanning, investigation and threat intelligence","Cybersecurity & Sentinel"),
]
_core_specs=[AgentSpec(n,r,d,False,()) for n,r,d in _core]
names={s.name for s in _core_specs}
_extra=[s for s in _specs if s.name not in names]
# Reserve 16 canonical legacy agent names without increasing the configured 2020-agent runtime.
ALL_AGENT_SPECS=_core_specs + _extra[16:]
assert len(ALL_AGENT_SPECS)==2020
DEFAULT_AGENTS=[Agent(s) for s in ALL_AGENT_SPECS]
AGENT_SPECS={s.name:s for s in ALL_AGENT_SPECS}
DEPARTMENT_COUNTS={d:sum(s.department==d for s in ALL_AGENT_SPECS) for d,_,_ in _DEPARTMENTS}
