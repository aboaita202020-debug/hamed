from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from .agent_bus import agent_bus
from .memory_store import memory_store
from .rd_agents import RD_AGENTS
from .science_agents import SCIENCE_AGENTS
from .social_agents import SOCIAL_AGENTS
from .stock_agents import STOCK_AGENTS
from .whale_agents import WHALE_AGENTS

CORE_TARGET=200

@dataclass
class LearningEvent:
    sender:str
    topic:str
    kind:str
    lesson:dict[str,Any]
    created_at:str

class CollectiveIntelligence:
    """Shared collaboration layer for the ORVIA agent network.
    Agents exchange help, evidence and verified lessons; unverified lessons are not promoted."""
    def __init__(self)->None:
        self.events:list[LearningEvent]=[]

    @property
    def total_configured_agents(self)->int:
        return CORE_TARGET+len(RD_AGENTS)+len(SCIENCE_AGENTS)+len(SOCIAL_AGENTS)+len(STOCK_AGENTS)+len(WHALE_AGENTS)

    def ask_help(self,sender:str,topic:str,recipients:list[str])->dict[str,Any]:
        msgs=agent_bus.broadcast(sender,"HELP",{"topic":topic,"request":"provide expertise and evidence"},recipients)
        return {"status":"help_requested","messages":len(msgs)}

    def share_lesson(self,sender:str,topic:str,lesson:dict[str,Any],recipients:list[str],verified:bool=False)->dict[str,Any]:
        if not verified:
            return {"status":"blocked","reason":"lesson_not_verified"}
        event=LearningEvent(sender,topic,"LEARN",lesson,datetime.now(timezone.utc).isoformat())
        self.events.append(event)
        memory_store.record("collective_learning",asdict(event),source=sender)
        msgs=agent_bus.broadcast(sender,"LEARN",{"topic":topic,"lesson":lesson},recipients)
        return {"status":"shared","recipients":len(msgs)}

    def peer_review(self,topic:str,claim:dict[str,Any],reviewers:list[str])->dict[str,Any]:
        msgs=agent_bus.broadcast("collective_intelligence","REVIEW",{"topic":topic,"claim":claim},reviewers)
        return {"status":"review_requested","reviewers":len(msgs)}

    def route(self,topic:str)->dict[str,Any]:
        t=topic.lower()
        selected=[]
        selected += [a.name for a in RD_AGENTS if ("github" in t or "tool" in t) and a.squad=="Discovery"][:5]
        selected += [a.name for a in SCIENCE_AGENTS if any(k in t for k in ("science","space","astronomy","physics","biology","math","ai"))][:10]
        selected += [a.name for a in SOCIAL_AGENTS if any(k in t for k in ("tiktok","instagram","youtube","facebook","reels","content"))][:10]
        selected += [a.name for a in STOCK_AGENTS if any(k in t for k in ("stock","stocks","market","بورصة","سهم","أسهم","portfolio","technical","fundamental","quant","options","futures"))][:15]
        selected += [a.name for a in WHALE_AGENTS if any(k in t for k in ("whale","flow","institution","institutional","large order","accumulation","distribution","حوت","تدفقات","مؤسسات"))][:10]
        if not selected:
            selected=[a.name for a in RD_AGENTS[:5]]
        return {"topic":topic,"selected_agents":selected,"dynamic_routing":True,"all_agents_run":False}

    def status(self)->dict[str,Any]:
        return {
            "core_target":CORE_TARGET,"rd_agents":len(RD_AGENTS),
            "science_agents":len(SCIENCE_AGENTS),"social_agents":len(SOCIAL_AGENTS),"stock_agents":len(STOCK_AGENTS),"whale_agents":len(WHALE_AGENTS),
            "total_configured_agents":self.total_configured_agents,
            "events":len(self.events),"shared_memory":True,
            "peer_review":True,"help_protocol":True,
            "learning_protocol":"discover_share_review_verify_teach",
        }

collective_intelligence=CollectiveIntelligence()
