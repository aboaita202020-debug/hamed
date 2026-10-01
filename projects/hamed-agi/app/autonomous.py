from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import ClassVar
from urllib.parse import urlparse

from .agi_engine import agi_engine
from .config import settings
from .crm import Customer, crm
from .memory_store import memory_store
from .models import Mission
from .opportunity import opportunity_engine
from .prospect_discovery import discover_prospects, discovery_runtime_status, discovery_provenance
from .reporting import daily_report
from .research import research


class AutonomousCommercialAgent:
    """Safe commercial operating loop: discover, research, qualify, draft, record, report.

    Search-result pages, articles, directories, government/report pages, social
    profile pages, and weak evidence are never promoted to qualified leads.
    """

    NON_BUSINESS_HOSTS: ClassVar[set[str]] = {
        "google.com", "bing.com", "duckduckgo.com", "html.duckduckgo.com",
        "facebook.com", "instagram.com", "tiktok.com", "youtube.com",
        "linkedin.com", "x.com", "twitter.com", "pinterest.com",
        "threads.net", "snapchat.com", "reddit.com", "wmtips.com",
    }
    NON_BUSINESS_TITLE_TERMS = (
        "search", "directory", "directories", "government", "gov",
        "country commercial guide", "report", "reports", "statistics",
        "news", "blog", "article", "articles", "marketplace directory",
        "top ", "list of", "best ", "review", "reviews",
    )
    NON_BUSINESS_PATH_TERMS = (
        "/search", "/directory", "/directories", "/blog", "/article",
        "/articles", "/reports/", "/report/", "/news/", "/news",
        "/country-commercial-guides/", "/statistics", "/technologies/",
    )

    @staticmethod
    def _prospect_name(url: str, title: str = "") -> str:
        if title:
            return title[:120]
        host = urlparse(url).netloc.lower().removeprefix("www.")
        return host or url

    @classmethod
    def _is_qualified_prospect(cls, evidence) -> tuple[bool, str]:
        url = str(getattr(evidence, "url", "") or "").strip()
        parsed = urlparse(url)
        host = parsed.netloc.lower().removeprefix("www.")
        title = str(getattr(evidence, "title", "") or "").strip().lower()
        notes = str(getattr(evidence, "notes", "") or "").strip().lower()

        if parsed.scheme not in {"http", "https"} or not host:
            return False, "invalid_public_url"
        if host in cls.NON_BUSINESS_HOSTS:
            return False, "non_business_host"
        path = (parsed.path or "").lower()
        if any(term in path for term in cls.NON_BUSINESS_PATH_TERMS):
            return False, "non_business_path"
        if any(term in title for term in cls.NON_BUSINESS_TITLE_TERMS):
            return False, "non_business_title"
        if "search evidence" in notes or "search result" in notes:
            return False, "search_only_evidence"
        if "direct site access unavailable" in notes:
            return False, "direct_site_access_unavailable"
        if getattr(evidence, "evidence_type", "") == "search_corroborated":
            return False, "identity_only_page_not_verified"
        if not getattr(evidence, "status_code", None) or not (200 <= evidence.status_code < 400):
            return False, "no_successful_business_page_fetch"
        return True, "qualified"

    def __init__(self) -> None:
        self.enabled = settings.autonomous_enabled

    @staticmethod
    def configured_urls() -> list[str]:
        raw = os.getenv("ORVIA_PROSPECT_URLS", "")
        return [u.strip() for u in raw.split(",") if u.strip()]

    def run_cycle(
        self,
        objective: str = "find commercial opportunities",
        urls: list[str] | None = None,
    ) -> dict:
        if not self.enabled:
            return {"status": "disabled", "reason": "autonomous_enabled=false"}

        started = datetime.now(timezone.utc).isoformat()
        mission = Mission(objective=objective, status="running")
        opportunities = []
        discovered_opportunities = opportunity_engine.discover(mission)

        targets = urls if urls is not None else self.configured_urls()
        discovery_mode = "configured_urls" if urls is not None or self.configured_urls() else "internet_discovery"
        if not targets:
            targets = discover_prospects(settings.autonomous_max_targets)

        discovery = discovery_runtime_status()
        researched = []
        leads = []
        offers = []
        rejected = []

        for url in targets[:settings.autonomous_max_targets]:
            provenance = discovery_provenance(url)
            evidence = research.fetch(url)
            evidence_dict = evidence.__dict__
            researched.append(evidence_dict)

            qualified, reason = self._is_qualified_prospect(evidence)
            if not qualified:
                rejected.append({
                    "url": url,
                    "reason": reason,
                    "title": getattr(evidence, "title", ""),
                })
                continue

            if not opportunities:
                opportunities = [agi_engine.analyze(x) for x in discovered_opportunities]

            name = self._prospect_name(url, evidence.title)
            customer = crm.upsert(Customer(
                name=name,
                contact=url,
                tags=["autonomous-prospect", "researched", "qualified"],
                metadata={
                    "source_url": url,
                    "last_researched_at": evidence.collected_at,
                    "qualification": "qualified",
                    "evidence": evidence_dict,
                },
            ))
            leads.append({
                "name": customer.name,
                "contact": customer.contact,
                "status": "qualified_for_review",
                "qualification": reason,
                "evidence": {
                    "title": evidence.title,
                    "url": evidence.url,
                    "collected_at": evidence.collected_at,
                    "notes": evidence.notes,
                    "evidence_type": getattr(evidence, "evidence_type", "unknown"),
                },
            })

            # Generate offers only after a real public business page has been
            # successfully fetched and qualified. The offer remains a draft;
            # outreach and irreversible actions stay behind approval.
            for opportunity in opportunities:
                offer = agi_engine.create_offer(
                    opportunity, prospect_name=customer.name
                )
                offers.append({
                    "prospect": customer.name,
                    "contact": customer.contact,
                    "subject": offer.subject,
                    "message": offer.message,
                    "service": offer.service,
                    "next_step": offer.next_step,
                    "evidence": [
                        *offer.evidence,
                        f"Research URL: {evidence.url}",
                        f"Evidence type: {getattr(evidence, 'evidence_type', 'unknown')}",
                        f"Research notes: {evidence.notes}",
                    ],
                    "status": "draft",
                    "approval_required_for_outreach": True,
                })

        completed_at = datetime.now(timezone.utc).isoformat()
        report = daily_report(
            {"status": "ok", "started_at": started, "completed_at": completed_at},
            [x.model_dump() for x in opportunities],
            crm.summary(),
            {},
        )
        result = {
            "status": "completed",
            "objective": objective,
            "discovery": {"mode": discovery_mode, **discovery},
            "researched": researched,
            "rejected": rejected,
            "opportunities": [x.model_dump() for x in opportunities],
            "leads": leads,
            "offers": offers,
            "report": report,
            "execution_policy": "no_purchase_payment_contract_or_irreversible_action",
        }
        memory_store.record(
            "autonomous_cycle", result, source="autonomous_commercial_agent"
        )
        return result


autonomous_agent = AutonomousCommercialAgent()
