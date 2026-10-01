from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SocialAgentSpec:
    name: str
    platform_group: str
    role: str
    capabilities: tuple[str,...]

GROUPS=[
 ("tiktok_instagram",50,[
  ("trend_scout",("trend_discovery","competitor_analysis")),
  ("idea_strategist",("idea_generation","audience_research")),
  ("script_writer",("short_form_script","hook_design")),
  ("retention_psychology",("retention","viewer_psychology")),
  ("storytelling",("storytelling","pacing")),
  ("producer_editor",("production","editing")),
  ("visuals",("visual_planning","creative_direction")),
  ("caption_seo",("caption","hashtags","metadata")),
  ("analytics_ab",("analytics","ab_testing")),
  ("quality_rights",("quality","rights","policy_review")),
 ]),
 ("facebook_youtube",50,[
  ("trend_scout",("trend_discovery","competitor_analysis")),
  ("audience_researcher",("audience_research","topic_demand")),
  ("script_writer",("long_form_script","short_form_script")),
  ("storytelling",("storytelling","retention")),
  ("producer_editor",("production","editing")),
  ("thumbnail_title",("thumbnail","title_optimization")),
  ("youtube_seo",("youtube_seo","metadata")),
  ("facebook_content",("facebook_posts","reels")),
  ("analytics_ab",("analytics","ab_testing")),
  ("quality_rights",("quality","rights","policy_review")),
 ])]

def build_social_agents()->list[SocialAgentSpec]:
    out=[]
    for group,count,roles in GROUPS:
        for i in range(count):
            role,caps=roles[i%len(roles)]
            out.append(SocialAgentSpec(f"{group}_{i+1:03d}",group,role,caps))
    assert len(out)==100
    return out

SOCIAL_AGENTS=build_social_agents()
SOCIAL_REGISTRY={a.name:a for a in SOCIAL_AGENTS}

def social_status()->dict[str,Any]:
    return {"count":100,"groups":{"tiktok_instagram":50,"facebook_youtube":50}}

def select_social_agents(platform_group:str|None=None,limit:int=20)->list[dict[str,Any]]:
    selected=SOCIAL_AGENTS if not platform_group else [a for a in SOCIAL_AGENTS if a.platform_group==platform_group]
    return [{"name":a.name,"platform_group":a.platform_group,"role":a.role,"capabilities":list(a.capabilities)} for a in selected[:max(1,min(limit,len(selected)))]]
