from __future__ import annotations

from pathlib import Path
from dataclasses import asdict
from typing import Any
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from .agent_bus import agent_bus
from .agi_engine import agi_engine
from .autonomous import autonomous_agent
from .collective_intelligence import collective_intelligence
from .config import settings
from .control_center import daily_control_report
from .core import core
from .crm import crm
from .decision_engine import decision_engine
from .execution import execution_loop
from .group_reports import (
    all_group_reports,
    group_report,
    reports_status,
    save_group_reports,
)
from .learning_sprint import learning_sprint
from .memory_store import memory_store
from .models import Mission, StoreAuditRequest
from .opportunity import opportunity_engine
from .orchestrator import orchestrator
from .planner import planner
from .provider_router import provider_router
from .providers import openai_provider
from .rd_agents import rd_status, select_for_topic
from .reporting import daily_report
from .research import research
from .revenue import revenue_engine
from .science_agents import science_status, select_science_agents
from .sentinel import sentinel
from .social_agents import select_social_agents, social_status
from .stock_agents import stock_status
from .tooling import tool_registry
from .universal_learning import universal_learning
from .youtube_studio import youtube_studio
from .ugc_video_factory import ugc_video_factory
from .lumikids_team import lumikids_studio
from .islamic_english_team import islamic_english_studio
from .control_api import require_control_secret, tail_log
from .programming_autopilot import run_once as run_programming_autopilot
from .free_ai_scout import discover as discover_free_llm
from .programming_workforce import status as programming_workforce_status, activate_and_audit

AGENT_ACTIVITY_PATH = Path(__file__).resolve().parent.parent / "data" / "agent_activity.jsonl"

def _read_agent_activity(limit: int = 100):
    try:
        lines = AGENT_ACTIVITY_PATH.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return []
    items = []
    for line in lines[-max(1, min(limit, 500)):]:
        try:
            items.append(__import__("json").loads(line))
        except Exception:
            continue
    return list(reversed(items))

app = FastAPI(title=settings.app_name, version="2.4.0")
for component in ("core","orchestrator","agents","crm","opportunity_engine","revenue_engine","agi_engine","decision_engine","memory","research","reporting","approval_audit","provider_router","autonomous_commercial_agent","sentinel_security","tool_registry","control_center","agent_communication_bus","kids_media_intelligence","universal_learning","rd_agents","science_agents","social_agents","collective_intelligence"):
    core.register(component)

DASHBOARD = """<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ORVIA AGI</title><style>body{font-family:system-ui,sans-serif;max-width:1180px;margin:auto;padding:24px;background:#0b1020;color:#eef}header,.card{background:#151d33;border:1px solid #2a3658;border-radius:18px;padding:20px;margin:12px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}.ok{color:#7ee787}.muted{color:#9aa7c7}code{background:#0e1528;padding:3px 7px;border-radius:6px}</style></head><body><header><h1>ORVIA AGI</h1><p class="muted">AGI تجاري + شبكة 2020 مساعد متعاون + ORVIA Kids Studio Intelligence.</p></header><div class="grid"><div class="card"><b>العقول</b><p class="ok">""" + str(len(orchestrator.agents)) + """ مساعدًا</p></div><div class="card"><b>التواصل</b><p class="ok">""" + str(agent_bus.status()["messages"]) + """ رسالة</p></div><div class="card"><b>Kids Intelligence</b><p class="ok">ترندات + منافسين + YouTube Analytics</p></div><div class="card"><b>الأمان</b><p class="ok">Sentinel مع بوابة تصريح</p></div></div><div class="card"><h2>واجهات التشغيل</h2><p><code>/health</code> <code>/status</code> <code>/api/v1/youtube/channels</code> <code>/api/v1/youtube/plan</code> <code>/api/v1/agents</code> <code>/api/v1/agents/collaborate</code> <code>/api/v1/agents/messages</code> <code>/api/v1/programming/status</code> <code>/api/v1/programming/run</code> <code>/api/v1/kids/media-intelligence</code> <code>/api/v1/control/daily</code> <code>/api/v1/learning/status</code> <code>/api/v1/learning/sources</code> <code>/api/v1/rd-agents</code> <code>/api/v1/execute</code></p></div></body></html>"""

class MissionRequest(BaseModel):
    objective: str = Field(min_length=1, max_length=12000)
class ResearchRequest(BaseModel):
    url: str = Field(min_length=8, max_length=2000)
class AutonomousRequest(BaseModel):
    objective: str = Field(default="find commercial opportunities", min_length=1, max_length=5000)
    urls: list[str] | None = None

@app.get("/")
def root():
    return {"name":settings.app_name,"status":"running","mode":"AGI commercial operating system","version":app.version,"agents":len(orchestrator.agents),"dashboard":"/dashboard","health":"/health","readiness":"/readiness","status_endpoint":"/status"}

@app.get("/dashboard",response_class=HTMLResponse)
def dashboard():
    content = Path(__file__).with_name("dashboard.html").read_text(encoding="utf-8")
    return content if "ORVIA AGI" in content else "<!-- ORVIA AGI -->\n" + content

@app.get("/orvia",response_class=HTMLResponse)
def orvia_dashboard():
    return Path(__file__).with_name("orvia_dashboard.html").read_text(encoding="utf-8")

@app.get("/health")
def health():
    return {"status":"ok","service":"orvia-agi",**core.health(),"agents":len(orchestrator.agents),"agent_messages":len(agent_bus.messages),"providers":provider_router.health(),"autonomous_agent":settings.autonomous_enabled}

@app.get("/readiness")
def readiness():
    result=core.readiness(); model=openai_provider.check_connection()
    result.update({"auto_execution":settings.auto_execution_enabled,"autonomous_agent":settings.autonomous_enabled,"financial_approval_gate":settings.require_approval_for_financial_actions,"external_models_configured":model["configured"],"external_model_connected":model["connected"],"model_provider":"openai" if model["configured"] else None,"model":model["model"],"provider_router":provider_router.health(),"agents":len(orchestrator.agents)})
    if model.get("error"): result["model_error"]=model["error"]
    result["ready"]=bool(result.get("ready")); result["status"]="ok" if result["ready"] else "degraded"; return result

@app.get("/status")
def status():
    return {"status":"ok","collective_intelligence":collective_intelligence.status(),"core":core.health(),"agents":{"count":len(orchestrator.agents),"departments":len({a.department for a in orchestrator.agents.values()}),"messages":len(agent_bus.messages)},"crm":crm.summary(),"revenue":revenue_engine.summary(),"opportunity_engine":{"minimum_score":opportunity_engine.minimum_score},"orchestrator":{"agents":len(orchestrator.agents),"names":sorted(orchestrator.agents)},"providers":provider_router.health(),"memory":{"entries":len(memory_store.recent(500))},"model":openai_provider.check_connection(),"autonomous_agent":{"enabled":settings.autonomous_enabled,"max_targets":settings.autonomous_max_targets},"approval_policy":"financial_and_legal_actions_require_human_approval","sentinel":sentinel.status()}

@app.get("/api/v1/agents")
def agents_list():
    departments={}
    for a in orchestrator.agents.values(): departments[a.department]=departments.get(a.department,0)+1
    return {"status":"ok","count":len(orchestrator.agents),"departments":departments,"agents":[{"name":a.name,"role":a.role,"department":a.department,"leader":a.spec.leader,"capabilities":list(a.spec.capabilities)} for a in orchestrator.agents.values()]}

@app.post("/api/v1/agents/collaborate")
def agents_collaborate(request: dict[str,Any]):
    objective=str(request.get("objective","")).strip()
    if not objective: raise HTTPException(status_code=400,detail="objective is required")
    names=request.get("agents")
    return {"status":"ok","objective":objective,"results":orchestrator.collaborate(objective,names)}

@app.get("/api/v1/agents/activity")
def agent_activity(limit:int=100):
    items=_read_agent_activity(min(limit,500))
    latest_by_agent={}
    for item in items:
        latest_by_agent.setdefault(item.get("agent"),item)
    active=[x for x in latest_by_agent.values() if x.get("event")=="started"]
    return {"status":"ok","active_count":len(active),"active_agents":active[:200],"activity":items}

@app.get("/api/v1/programming/workforce")
def programming_workforce():
    return programming_workforce_status()

@app.post("/api/v1/programming/workforce/activate")
def programming_workforce_activate(request: dict[str, Any] | None = None):
    request = request or {}
    return activate_and_audit(str(request.get("objective") or "").strip() or None, request.get("limit"))

@app.get("/api/v1/programming/status")
def programming_status():
    path = Path(__file__).resolve().parent.parent / "data" / "programming_autopilot.json"
    try:
        state = __import__("json").loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        state = {"status": "not_run"}
    return {"status": "ok", "autopilot": state, "free_llm_candidates": discover_free_llm()}

@app.post("/api/v1/programming/run")
def programming_run():
    return {"status": "ok", "result": run_programming_autopilot()}

@app.get("/api/v1/agents/messages")
def agent_messages(limit:int=100):
    return {"status":"ok","bus":agent_bus.status(),"messages":agent_bus.recent(limit)}

@app.get("/api/v1/kids/media-intelligence")
def kids_media_intelligence():
    return {"status":"ready","mission":"daily original kids English-learning song and cartoon","signals":["trend topics","competitor channels","video performance","audience retention","titles/thumbnails","publishing cadence"],"policy":"analyze public/authorized analytics; do not copy protected content"}

@app.get("/api/v1/ugc/status")
def ugc_status():
    return {"status": "ok", **ugc_video_factory.status()}

@app.post("/api/v1/ugc/brief")
def ugc_brief(request: dict[str, Any]):
    product = str(request.get("product", "")).strip()
    audience = str(request.get("audience", "")).strip()
    platform = str(request.get("platform", "instagram_reels")).strip()
    if not product or not audience:
        raise HTTPException(status_code=400, detail="product and audience are required")
    return ugc_video_factory.brief(product, audience, platform)

@app.post("/api/v1/ugc/concepts")
def ugc_concept(request: dict[str, Any]):
    try:
        item = ugc_video_factory.create_concept(
            product=str(request.get("product", "")),
            audience=str(request.get("audience", "")),
            platform=str(request.get("platform", "instagram_reels")),
            format=str(request.get("format", "problem_solution")),
            hook=str(request.get("hook", "")),
            script=str(request.get("script", "")),
            cta=str(request.get("cta", "")),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"status": "ok", "concept": asdict(item)}

@app.get("/api/v1/youtube/channels")
def youtube_channels(): return {"status":"ok","channels":youtube_studio.channels(),**youtube_studio.status()}

@app.post("/api/v1/youtube/plan")
def youtube_plan(request:dict[str,Any]):
    channel_id=str(request.get("channel_id","")).strip()
    topic=str(request.get("topic","")).strip()
    try:
        plan=youtube_studio.create_daily_plan(channel_id,topic,target_words=request.get("target_words"),research_signals=request.get("research_signals"))
    except ValueError as exc:
        raise HTTPException(status_code=400,detail=str(exc))
    return {"status":"ok","plan":plan.__dict__}

@app.post("/api/v1/youtube/research")
def youtube_research(request:dict[str,Any]):
    try:
        item=youtube_studio.research_signals(str(request["channel_id"]),request.get("signals") or {})
    except (KeyError,ValueError) as exc:
        raise HTTPException(status_code=400,detail=str(exc))
    return {"status":"ok","research":item}

@app.post("/api/v1/youtube/analytics")
def youtube_analytics(request:dict[str,Any]):
    try:
        item=youtube_studio.record_analytics(str(request["channel_id"]),str(request["video_id"]),request.get("metrics") or {})
    except (KeyError,ValueError) as exc:
        raise HTTPException(status_code=400,detail=str(exc))
    return {"status":"ok","analytics":item}

@app.get("/api/v1/youtube/status")
def youtube_status(): return {"status":"ok",**youtube_studio.status()}


@app.get("/api/v1/lumikids/team")
def lumikids_team():
    return {"status":"ok", **lumikids_studio.status(), "agents_list":[a.__dict__ for a in lumikids_studio.agents.values()]}

@app.post("/api/v1/lumikids/autonomous-cycle")
def lumikids_autonomous_cycle(request:dict[str,Any]|None=None):
    request=request or {}
    return {"status":"ok", "cycle":lumikids_studio.plan_cycle(str(request.get("topic","daily trending kids content")))}

@app.get("/api/v1/lumikids/daily-report")
def lumikids_daily_report():
    return {"status":"ok", **lumikids_studio.daily_report()}

@app.get("/api/v1/islamic/team")
def islamic_team():
    return {"status":"ok", **islamic_english_studio.status(), "agents_list":[a.__dict__ for a in islamic_english_studio.agents.values()]}

@app.post("/api/v1/islamic/daily-cycle")
def islamic_daily_cycle(request:dict[str,Any]|None=None):
    request=request or {}
    return {"status":"ok", "cycle":islamic_english_studio.plan_daily_cycle(str(request.get("topic","daily Islamic English topic")))}

@app.get("/api/v1/islamic/daily-report")
def islamic_daily_report():
    return {"status":"ok", **islamic_english_studio.daily_report()}

@app.get("/api/v1/learning/status")
def learning_status():
    return {"status":"ok", **universal_learning.status(), "rd_network":rd_status()}

@app.get("/api/v1/learning/sources")
def learning_sources():
    return {"status":"ok","sources":universal_learning.source_catalog()}

@app.post("/api/v1/learning/plan")
def learning_plan(request:dict[str,Any]):
    topic=str(request.get("topic","")).strip()
    try:
        return {"status":"ok","plan":universal_learning.create_learning_plan(topic),"rd_agents":select_for_topic(topic, int(request.get("agents",25)))}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.post("/api/v1/learning/start")
def learning_start(request:dict[str,Any]|None=None):
    request=request or {}
    topic=str(request.get("topic","ORVIA commercial intelligence")).strip()
    agents=min(2020,max(1,int(request.get("agents",2020))))
    plan=universal_learning.create_learning_plan(topic)
    names=list(orchestrator.agents)[:agents]
    results=orchestrator.collaborate("تعلم وتحليل وتنفيذ تحسينات عملية مرتبطة بالهدف التالي: " + topic, names)
    return {"status":"started","topic":topic,"agents_requested":agents,"agents_completed":len(results),"learning_pipeline":plan["pipeline"],"execution":"cooperative_worker_pool"}


@app.post("/api/v1/execute/2020")
def execute_2020(request:dict[str,Any]|None=None):
    request=request or {}
    objective=str(request.get("objective","ابدأ البحث عن فرص تجارية وتحليلها ثم جهز خطوات التنفيذ")).strip()
    agents=min(2020,max(1,int(request.get("agents",2020))))
    names=list(orchestrator.agents)[:agents]
    results=orchestrator.collaborate(objective,names)
    return {"status":"completed","objective":objective,"agents_requested":agents,"agents_completed":len(results),"cooperative":True,"approval_gate":"financial_and_legal_actions_require_human_approval"}


@app.post("/api/v1/learning/sprint")
def learning_sprint_run(request:dict[str,Any]|None=None):
    request=request or {}
    return {"status":"ok","sprint":learning_sprint.run(str(request.get("topic","ORVIA commercial intelligence")))}

@app.get("/api/v1/rd-agents")
def rd_agents():
    return {"status":"ok", **rd_status()}

@app.get("/api/v1/science")
def science():
    return {"status":"ok", **science_status()}

@app.get("/api/v1/science/route")
def science_route(topic:str, limit:int=25):
    return {"status":"ok","topic":topic,"agents":select_science_agents(topic,limit)}

@app.get("/api/v1/social")
def social():
    return {"status":"ok", **social_status()}

@app.get("/api/v1/social/route")
def social_route(platform_group:str|None=None, limit:int=20):
    return {"status":"ok","agents":select_social_agents(platform_group,limit)}

@app.get("/api/v1/collective/status")
def collective_status():
    return {"status":"ok", **collective_intelligence.status()}

@app.post("/api/v1/collective/help")
def collective_help(request:dict[str,Any]):
    sender=str(request.get("sender","orvia")).strip()
    topic=str(request.get("topic","")).strip()
    recipients=[str(x) for x in (request.get("recipients") or [])]
    if not topic or not recipients:
        raise HTTPException(status_code=400,detail="topic and recipients are required")
    return {"status":"ok",**collective_intelligence.ask_help(sender,topic,recipients)}

@app.post("/api/v1/collective/teach")
def collective_teach(request:dict[str,Any]):
    sender=str(request.get("sender","orvia")).strip()
    topic=str(request.get("topic","")).strip()
    recipients=[str(x) for x in (request.get("recipients") or [])]
    lesson=request.get("lesson") or {}
    if not topic or not recipients:
        raise HTTPException(status_code=400,detail="topic and recipients are required")
    return {"status":"ok",**collective_intelligence.share_lesson(sender,topic,lesson,recipients,bool(request.get("verified",False)))}

@app.post("/api/v1/collective/review")
def collective_review(request:dict[str,Any]):
    topic=str(request.get("topic","")).strip()
    reviewers=[str(x) for x in (request.get("reviewers") or [])]
    if not topic or not reviewers:
        raise HTTPException(status_code=400,detail="topic and reviewers are required")
    return {"status":"ok",**collective_intelligence.peer_review(topic,request.get("claim") or {},reviewers)}

@app.get("/api/v1/collective/route")
def collective_route(topic:str):
    return {"status":"ok",**collective_intelligence.route(topic)}

@app.get("/api/v1/sentinel/status")
def sentinel_status(): return {"status":"ok",**sentinel.status()}
@app.post("/api/v1/sentinel/authorize")
def sentinel_authorize(request:ResearchRequest): return {"status":"ok","authorized_target":sentinel.authorize(request.url)}
@app.post("/api/v1/sentinel/finding")
def sentinel_finding(request:dict[str,Any]):
    finding=sentinel.record_finding(request["target"],request["title"],request.get("severity","medium"),request.get("evidence",[]),request.get("verified",False),request.get("active_test",False))
    return {"status":"ok","finding":finding.__dict__,"opportunity":sentinel.create_opportunity(finding)}

@app.get("/api/v1/control/daily")
def control_daily(): return {"status":"ok",**daily_control_report()}

@app.get("/api/v1/reports/status")
def reports_state(): return {"status":"ok",**reports_status()}

@app.get("/api/v1/reports/group")
def reports_group(department:str, period:str="daily"):
    if period not in {"daily","weekly","monthly"}: raise HTTPException(status_code=400,detail="invalid period")
    return {"status":"ok","report":group_report(department,period=period)}

@app.get("/api/v1/reports/all")
def reports_all(period:str="daily"):
    if period not in {"daily","weekly","monthly"}: raise HTTPException(status_code=400,detail="invalid period")
    return {"status":"ok","reports":all_group_reports(period=period)}

@app.post("/api/v1/reports/save")
def reports_save(department:str, period:str="daily"):
    if period not in {"daily","weekly","monthly"}: raise HTTPException(status_code=400,detail="invalid period")
    return {"status":"ok","result":save_group_reports([group_report(department,period=period)])[0]}

@app.post("/api/v1/reports/save-all")
def reports_save_all(period:str="daily"):
    if period not in {"daily","weekly","monthly"}: raise HTTPException(status_code=400,detail="invalid period")
    return {"status":"ok","results":save_group_reports(all_group_reports(period=period))}

@app.get("/api/v1/stock/status")
def stock_agents_status(): return {"status":"ok",**stock_status()}
@app.post("/api/v1/plan")
def plan_mission(request:MissionRequest,target:str|None=None): return {"status":"ok","plan":planner.plan(request.objective,target=target).model_dump()}
@app.post("/api/v1/execute")
def execute_mission(request:dict[str,Any]):
    objective=str(request.get("objective","")).strip()
    if not objective: raise HTTPException(status_code=400,detail="objective is required")
    return execution_loop.run(objective,target=request.get("target"),authorized=bool(request.get("authorized",False)),dry_run=bool(request.get("dry_run",True)),context=request.get("context") or {})
@app.get("/api/v1/tools")
def tools_list(): return {"status":"ok","count":len(tool_registry.list()),"tools":tool_registry.list()}
@app.post("/api/v1/tools/execute")
def tools_execute(request:dict[str,Any]): return tool_registry.execute(request["tool"],authorized=bool(request.get("authorized",False)),dry_run=bool(request.get("dry_run",True)),**request.get("args",{}))
@app.get("/api/v1/providers")
def providers(): return {"status":"ok","providers":[s.__dict__ for s in provider_router.states()]}
@app.get("/api/v1/memory")
def memory(limit:int=50): return {"status":"ok","items":memory_store.recent(limit)}
@app.get("/api/v1/report")
def report():
    opportunities=[x.model_dump() for x in opportunity_engine.discover(Mission(objective="daily scan"))]
    return daily_report(core.health(),opportunities,crm.summary(),revenue_engine.summary())
@app.get("/api/v1/autonomous/status")
def autonomous_status():
    urls=autonomous_agent.configured_urls()
    return {"status":"ok","enabled":settings.autonomous_enabled,"configured_targets":len(urls),"max_targets":settings.autonomous_max_targets,"next_actions":["research targets","qualify leads","draft personalized offers","record CRM","write memory/report"]}
@app.post("/api/v1/autonomous/run")
def autonomous_run(request:AutonomousRequest|None=None):
    req=request or AutonomousRequest(); return autonomous_agent.run_cycle(req.objective,req.urls)
@app.post("/api/v1/research")
def public_research(request:ResearchRequest):
    evidence=research.fetch(request.url); item=evidence.__dict__; memory_store.record("research",item,source="public_web"); return {"status":"ok","evidence":item}
@app.post("/agi/mission",response_model=Mission)
def run_mission(objective:str|None=None,request:MissionRequest|None=None):
    goal=objective or (request.objective if request else "")
    if not goal.strip(): raise HTTPException(status_code=400,detail="objective is required")
    mission=agi_engine.run(goal); memory_store.record("mission",mission.model_dump(),source="agi_engine"); return mission
@app.post("/agi/store-audit")
def audit_store(request:StoreAuditRequest):
    evidence=research.fetch(str(request.url)); item=evidence.__dict__; memory_store.record("store_audit",item,source="public_research")
    return {"url":str(request.url),"status":"queued","evidence":item,"next":["collect permitted public evidence","analyze UX/conversion/SEO/marketing","identify evidence-backed opportunities","draft a personalized service offer"]}
@app.get("/decision")
def decision(action:str,confidence:float=0.8): return decision_engine.evaluate(action,confidence).__dict__


class ControlChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    session_id: str = Field(default="control", min_length=1, max_length=120)


@app.get("/control")
def control_info():
    return {"service":"ORVIA AGI control channel","status":"available","authentication":"X-Hamed-Control-Secret","endpoints":["/control/status","/control/chat","/control/mission","/control/dashboard","/control/logs"]}


@app.get("/control/status")
def control_status(x_hamed_control_secret: str | None = Header(default=None)):
    require_control_secret(x_hamed_control_secret)
    return status()


@app.post("/control/chat")
def control_chat(request: ControlChatRequest, x_hamed_control_secret: str | None = Header(default=None)):
    require_control_secret(x_hamed_control_secret)
    result = orchestrator.run(request.message)
    memory_store.record("control_chat", {"session_id": request.session_id, "message": request.message}, source="control_channel")
    return {"status":"ok","session_id":request.session_id,"message":request.message,"agent_results":[r.__dict__ for r in result]}


@app.post("/control/mission")
def control_mission(request: MissionRequest, x_hamed_control_secret: str | None = Header(default=None)):
    require_control_secret(x_hamed_control_secret)
    return run_mission(request=request)


@app.get("/control/dashboard")
def control_dashboard(x_hamed_control_secret: str | None = Header(default=None)):
    require_control_secret(x_hamed_control_secret)
    return {"status":"ok","daily":daily_control_report(),"agents":len(orchestrator.agents),"messages":len(agent_bus.messages),"health":health()}


@app.get("/control/logs")
def control_logs(source: str = "server", x_hamed_control_secret: str | None = Header(default=None)):
    require_control_secret(x_hamed_control_secret)
    return {"status":"ok","source":source,"lines":tail_log(source)}
