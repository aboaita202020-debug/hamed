from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ScienceAgentSpec:
    name: str
    domain: str
    capabilities: tuple[str, ...]
    evidence_policy: str = "peer_review_primary_sources_cross_check"

SCIENCE_DOMAINS = [
 ("astronomy_space",60,("astronomy","astrophysics","space_science")),
 ("physics",80,("physics","mathematical_physics","simulation")),
 ("chemistry",70,("chemistry","materials","analytical_science")),
 ("biology_life_sciences",80,("biology","genetics","ecology")),
 ("neuroscience_cognition",40,("neuroscience","cognition","brain_science")),
 ("earth_climate",60,("geoscience","climate","earth_systems")),
 ("mathematics_statistics",70,("mathematics","statistics","probability")),
 ("computer_science_ai",90,("computer_science","ai","machine_learning")),
 ("robotics_autonomous",40,("robotics","autonomy","control")),
 ("engineering",90,("engineering","systems","design")),
 ("medical_pharma_science",60,("medical_research","pharmacology","biomedical_science")),
 ("psychology_behavioral",40,("psychology","behavioral_science","experimental_design")),
 ("economics_finance",40,("economics","finance","econometrics")),
 ("history_archaeology_humanities",30,("history","archaeology","humanities")),
 ("languages_linguistics",30,("linguistics","languages","computational_linguistics")),
 ("agriculture_food_environment",30,("agriculture","food_science","environment")),
 ("law_public_policy_knowledge",10,("law_research","public_policy","regulatory_analysis")),
 ("education_learning_sciences",10,("education","learning_science","pedagogy")),
 ("interdisciplinary_research",70,("interdisciplinary","systems_thinking","research_methods")),
]

def build_science_agents() -> list[ScienceAgentSpec]:
    result=[]
    for domain,count,caps in SCIENCE_DOMAINS:
        for i in range(count):
            result.append(ScienceAgentSpec(f"science_{domain}_{i+1:03d}",domain,caps))
    assert len(result)==1000
    assert len({a.name for a in result})==1000
    return result

SCIENCE_AGENTS=build_science_agents()
SCIENCE_REGISTRY={a.name:a for a in SCIENCE_AGENTS}

def science_status()->dict[str,Any]:
    domains={d:c for d,c,_ in SCIENCE_DOMAINS}
    return {"count":1000,"domains":domains,"astronomy_agents":70}

def select_science_agents(topic:str,limit:int=25)->list[dict[str,Any]]:
    t=topic.lower()
    aliases={"space":"astronomy_space","astronomy":"astronomy_space","physics":"physics","math":"mathematics_statistics","ai":"computer_science_ai","biology":"biology_life_sciences","medicine":"medical_pharma_science","psychology":"psychology_behavioral"}
    domain=next((v for k,v in aliases.items() if k in t),None)
    selected=SCIENCE_AGENTS if not domain else [a for a in SCIENCE_AGENTS if a.domain==domain]
    return [{"name":a.name,"domain":a.domain,"capabilities":list(a.capabilities)} for a in selected[:max(1,min(limit,len(selected)))]]


# Historical alchemy specialization: 100 of the existing 1,000 science agents.
ALCHEMY_ALLOCATION = {"chemistry": 70, "history_archaeology_humanities": 15, "interdisciplinary_research": 15}
ALCHEMY_FOCUS = (
    "Egyptian and Hellenistic alchemy",
    "Arabic and Islamic alchemical traditions",
    "European medieval alchemy",
    "Chinese alchemy",
    "Indian alchemical traditions",
    "manuscripts, symbols and terminology",
    "metals and historical transformation theories",
    "elixirs and historical alchemical medicine",
    "philosophy and theories of alchemy",
    "comparison with modern chemistry",
)

def alchemy_agents() -> list[ScienceAgentSpec]:
    selected = [a for a in SCIENCE_AGENTS if a.domain == "chemistry"]
    selected += [a for a in SCIENCE_AGENTS if a.domain == "history_archaeology_humanities" and int(a.name.rsplit("_", 1)[-1]) <= 15]
    selected += [a for a in SCIENCE_AGENTS if a.domain == "interdisciplinary_research" and int(a.name.rsplit("_", 1)[-1]) <= 15]
    assert len(selected) == 100
    assert len({a.name for a in selected}) == 100
    return selected

ALCHEMY_AGENTS = alchemy_agents()
ALCHEMY_REGISTRY = {a.name: a for a in ALCHEMY_AGENTS}

def alchemy_status() -> dict[str, Any]:
    return {
        "count": 100,
        "total_science_network": 1000,
        "unique_agents": True,
        "focus": list(ALCHEMY_FOCUS),
        "allocation": dict(ALCHEMY_ALLOCATION),
        "method": "historical sources + archaeology + comparative scholarship + modern-science cross-check",
    }

def select_alchemy_agents(topic: str = "", limit: int = 25) -> list[dict[str, Any]]:
    t = topic.lower().strip()
    keys = {
        "egypt": "history_archaeology_humanities",
        "hellenistic": "history_archaeology_humanities",
        "arabic": "interdisciplinary_research",
        "islamic": "interdisciplinary_research",
        "china": "history_archaeology_humanities",
        "india": "history_archaeology_humanities",
        "manuscript": "history_archaeology_humanities",
        "chemistry": "chemistry",
    }
    domain = next((v for k, v in keys.items() if k in t), None)
    selected = ALCHEMY_AGENTS if domain is None else [a for a in ALCHEMY_AGENTS if a.domain == domain]
    selected = selected[:max(1, min(limit, len(selected)))]
    return [{"name": a.name, "domain": a.domain, "capabilities": list(a.capabilities)} for a in selected]


