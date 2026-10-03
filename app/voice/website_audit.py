"""Evidence-first website audit used by Hamed before sales outreach.

This module intentionally does not scrape restricted content or invent findings.
It accepts observations produced by an authorized fetcher and converts them into
commercially useful, evidence-backed findings.
"""
from dataclasses import dataclass, asdict
from typing import Any, Iterable


@dataclass(frozen=True)
class AuditFinding:
    category: str
    severity: str
    observation: str
    evidence: str
    business_impact: str
    suggested_service: str


@dataclass(frozen=True)
class WebsiteAudit:
    url: str
    findings: tuple[AuditFinding, ...]
    strengths: tuple[str, ...] = ()

    @property
    def commercial_opportunities(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(f.suggested_service for f in self.findings if f.suggested_service))

    def to_dict(self) -> dict[str, Any]:
        return {
            "url": self.url,
            "strengths": list(self.strengths),
            "findings": [asdict(f) for f in self.findings],
            "commercial_opportunities": list(self.commercial_opportunities),
        }


def build_audit(
    url: str,
    observations: Iterable[dict[str, str]],
    strengths: Iterable[str] = (),
) -> WebsiteAudit:
    """Turn verified observations into an audit; never fabricate missing evidence."""
    findings: list[AuditFinding] = []
    for item in observations:
        if not item.get("observation") or not item.get("evidence"):
            continue
        findings.append(
            AuditFinding(
                category=item.get("category", "general"),
                severity=item.get("severity", "medium"),
                observation=item["observation"],
                evidence=item["evidence"],
                business_impact=item.get("business_impact", "").strip(),
                suggested_service=item.get("suggested_service", "").strip(),
            )
        )
    return WebsiteAudit(url=url, findings=tuple(findings), strengths=tuple(strengths))
