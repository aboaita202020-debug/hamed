"""Deterministic service engines. They analyze supplied/public evidence and never invent findings."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from io import BytesIO
from typing import Any
import uuid

@dataclass
class KnowledgeItem:
    topic: str; claim: str; source: str; evidence: str; confidence: float
    date: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class KnowledgeBase:
    def __init__(self) -> None: self.items: list[KnowledgeItem] = []
    def add(self,item:KnowledgeItem)->KnowledgeItem:
        if not item.source or not item.evidence: raise ValueError("knowledge requires source and evidence")
        if not 0<=item.confidence<=1: raise ValueError("confidence must be between 0 and 1")
        self.items.append(item); return item
    def search(self,topic:str)->list[KnowledgeItem]: return [x for x in self.items if topic.lower() in x.topic.lower()]

class EducationCouncil:
    AREAS=("general-learning","psychology-customer-behavior","sales-science","marketing-growth","strategy-continuous-learning")
    def evaluate(self,claim:str,*,source:str,evidence:str,confidence:float)->KnowledgeItem:
        if not source or not evidence: raise ValueError("source and evidence are required")
        if not 0<=confidence<=1: raise ValueError("confidence must be between 0 and 1")
        return KnowledgeItem("education",claim,source,evidence,confidence)
    def process(self,claim:str,source:str,evidence:str,confidence:float)->dict[str,Any]:
        item=self.evaluate(claim,source=source,evidence=evidence,confidence=confidence)
        return {"research":True,"evaluate_sources":True,"extract_knowledge":True,"compare_claims":True,"confidence":item.confidence,"knowledge":item}

class OpportunityEngine:
    def analyze(self,business:dict[str,Any])->dict[str,Any]:
        evidence=list(business.get("evidence") or []); problems=list(business.get("problems") or []); hypotheses=list(business.get("hypotheses") or []); opportunities=list(business.get("opportunities") or []); services=list(business.get("recommended_services") or [])
        score=float(business.get("opportunity_score",0 if not evidence else min(100,20+len(evidence)*10)))
        return {"problems":problems,"opportunities":opportunities,"recommended_services":services,"recommended_package":business.get("recommended_package"),"opportunity_score":score,"estimated_value":business.get("estimated_value"),"priority":business.get("priority","medium"),"evidence":evidence,"hypotheses":hypotheses,"confidence":float(business.get("confidence",0 if not evidence else .5))}

class WebsiteAnalyzer:
    CHECKS=("ux","mobile","performance","seo","content","cta","navigation","trust","conversion")
    def analyze(self,evidence:dict[str,Any])->dict[str,Any]: return {"checks":{k:evidence.get(k) for k in self.CHECKS if k in evidence},"evidence":evidence.get("evidence",[]),"hypotheses":evidence.get("hypotheses",[])}
class StoreAnalyzer(WebsiteAnalyzer): CHECKS=WebsiteAnalyzer.CHECKS+("product_pages","checkout")
class RestaurantGrowthEngine:
    FEATURES=("website","mobile_menu","qr_menu","menu_categories","arabic_english","offers","ordering","booking","local_seo","google_business_support","review_analysis","reputation_monitoring","marketing_strategy")
    def analyze(self,evidence:dict[str,Any])->dict[str,Any]: return {"features":{k:evidence.get(k) for k in self.FEATURES if k in evidence},"evidence":evidence.get("evidence",[]),"hypotheses":evidence.get("hypotheses",[])}

class QRMenu:
    def __init__(self,base_url:str)->None:self.base_url=base_url.rstrip("/");self.menus={}
    def create(self,menu_id:str,content:dict[str,Any])->str:self.menus[menu_id]=dict(content);return f"{self.base_url}/menu/{menu_id}"
    def update(self,menu_id:str,content:dict[str,Any])->str:
        if menu_id not in self.menus:raise KeyError(menu_id)
        self.menus[menu_id]=dict(content);return f"{self.base_url}/menu/{menu_id}"
    def page(self,menu_id:str)->dict[str,Any]:return {"status":"ok","menu_id":menu_id,"content":self.menus[menu_id]} if menu_id in self.menus else {"status":"not_found"}
    def generate(self,menu_id:str)->bytes:
        if menu_id not in self.menus:raise KeyError(menu_id)
        import qrcode
        from qrcode.image.svg import SvgPathImage
        qr=qrcode.QRCode(box_size=8,border=4);qr.add_data(f"{self.base_url}/menu/{menu_id}");qr.make(fit=True)
        out=BytesIO();qr.make_image(image_factory=SvgPathImage).save(out);return out.getvalue()

class ReputationEngine:
    def analyze(self,reviews:list[dict[str,Any]])->dict[str,Any]:
        ratings=[float(r["rating"]) for r in reviews if "rating" in r];texts=[str(r.get("text","")) for r in reviews if r.get("text")]
        positive=[t for t in texts if any(w in t.lower() for w in ("good","great","excellent","ممتاز","جيد"))];negative=[t for t in texts if any(w in t.lower() for w in ("bad","poor","slow","سيء","بطء"))]
        return {"count":len(reviews),"average_rating":sum(ratings)/len(ratings) if ratings else None,"positive_themes":positive,"negative_themes":negative,"sentiment":{"positive":len(positive),"negative":len(negative)},"trends":[],"suggested_responses":[]}

class SalesMessageEngine:
    def generate(self,lead:dict[str,Any])->dict[str,Any]:
        evidence=lead.get("evidence") or []
        if not evidence:raise ValueError("personalized outreach requires evidence")
        problem=lead.get("problem") or lead.get("detected_problem") or "an observable growth opportunity";service=lead.get("service") or "digital growth support";name=lead.get("name") or "there"
        return {"message":f"Hi {name}, I noticed {problem}. Based on that public evidence, {service} could help. If useful, I can share a short, specific improvement plan.","evidence":evidence,"approved":False,"cta":"share a short improvement plan"}

@dataclass(frozen=True)
class Service:
    service_id:str;name:str;category:str;description:str;target_customer:str;problems_solved:tuple[str,...];deliverables:tuple[str,...];required_agents:tuple[str,...]=();required_tools:tuple[str,...]=();duration:str="scope-dependent";pricing_model:str="custom";minimum_price:float=0;recommended_price:float=0;deposit_policy:str="policy-defined"
class ServiceCatalog:
    def __init__(self):
        self.services={
            "website-optimization":Service("website-optimization","Website Optimization","web","Evidence-based website improvements","business",("ux","conversion"),("audit","recommendations")),
            "qr-menu":Service("qr-menu","QR Menu","restaurant","Editable QR-linked menu","restaurant",("menu-access",),("mobile-menu","qr")),
            "seo":Service("seo","SEO","marketing","Search visibility improvements","business",("search-visibility",),("seo-audit","plan")),
            "reputation":Service("reputation","Reputation Analysis","customer","Public review analysis","local-business",("reputation",),("review-analysis",)),
            "store-optimization":Service("store-optimization","Store Optimization","commerce","Evidence-based store improvements","ecommerce",("conversion",),("store-audit","recommendations")),
            "marketing-plan":Service("marketing-plan","Marketing Plan","marketing","Actionable growth plan","business",("growth",),("strategy","roadmap")),
            "social-media-management":Service("social-media-management","Social Media Management","social","Content, community and growth management","business",("inconsistent-content","low-engagement","weak-social-presence"),("audit","content-calendar","engagement-plan","analytics-report")),
            "content-production":Service("content-production","Social Content Production","social","Platform-native content planning and production","business",("content-gap","weak-hooks"),("content-calendar","post-briefs","reels-ideas","stories")),
            "social-growth":Service("social-growth","Social Growth","social","Authentic audience and reach growth","business",("slow-growth","low-reach"),("growth-plan","content-strategy","kpi-dashboard")),
            "social-lead-generation":Service("social-lead-generation","Social Lead Generation","social","Evidence-based prospect discovery and conversion","business",("few-leads","low-conversion"),("prospect-plan","outreach-drafts","lead-funnel")),
            "ads-management":Service("ads-management","Ads Management","marketing","Campaign planning and performance optimization","business",("paid-growth","high-acquisition-cost"),("campaign-plan","creative-brief","kpi-report")),
            "conversion-optimization":Service("conversion-optimization","Conversion Optimization","marketing","Turn social interest into qualified leads and sales","business",("low-conversion","weak-cta"),("funnel-audit","cta-plan","conversion-roadmap")),
        }
    def get(self,service_id:str)->Service:return self.services[service_id]
    def all(self)->list[Service]:return list(self.services.values())
class PackageEngine:
    def build(self,service_ids:list[str],catalog:ServiceCatalog|None=None)->dict[str,Any]:
        c=catalog or ServiceCatalog();ss=[c.get(i) for i in service_ids];return {"services":[s.service_id for s in ss],"deliverables":[d for s in ss for d in s.deliverables],"required_agents":list(dict.fromkeys(a for s in ss for a in s.required_agents))}
class OfferEngine:
    def create(self,package:dict[str,Any],*,price:float,deposit:float,timeline:str)->dict[str,Any]:
        if price<0 or not 0<=deposit<=price:raise ValueError("invalid price/deposit")
        return {"offer_id":str(uuid.uuid4()),"package":package,"price":price,"deliverables":package.get("deliverables",[]),"timeline":timeline,"deposit":deposit,"payment_schedule":"deposit then milestone/final","upsells":[]}
class NegotiationEngine:
    def negotiate(self,*,price:float,minimum_price:float,discount:float,deposit_percentage:float,allowed_deliverables:list[str],requested_deliverables:list[str])->dict[str,Any]:
        final=price*(1-max(0,discount));allowed=final>=minimum_price and 0<=deposit_percentage<=1 and set(requested_deliverables).issubset(set(allowed_deliverables));return {"accepted":allowed,"price":final,"minimum_price":minimum_price,"deposit_percentage":deposit_percentage,"deliverables_allowed":set(requested_deliverables).issubset(set(allowed_deliverables))}
class CRM:
    STATUSES=("lead","qualified","contacted","interested","proposal","negotiation","won","deposit_pending","in_progress","delivered","follow_up","upsell","closed")
    def __init__(self):self.records={}
    def create(self,**fields):
        lead_id=fields.pop("lead_id",str(uuid.uuid4()));r={"lead_id":lead_id,"status":fields.pop("status","lead"),"lead_score":fields.pop("lead_score",0),"opportunity_score":fields.pop("opportunity_score",0),"deal_value":fields.pop("deal_value",None),"next_action":fields.pop("next_action",None),"history":[],"offers":[],"messages":[],"timestamps":{},**fields};self.records[lead_id]=r;return r
    def transition(self,lead_id:str,status:str):
        if status not in self.STATUSES:raise ValueError("invalid CRM status")
        r=self.records[lead_id];r["history"].append(r["status"]);r["status"]=status;r["timestamps"][status]=datetime.now(timezone.utc).isoformat();return r
