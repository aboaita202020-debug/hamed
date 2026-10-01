from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse


@dataclass
class SecurityFinding:
    target: str
    title: str
    severity: str
    status: str
    evidence: list[str]
    source: str = "sentinel"
    verified: bool = False


class Sentinel:
    """Defensive security opportunity engine.

    Active testing is intentionally limited to explicitly authorized targets.
    Public research and threat-intelligence signals can be recorded for other
    targets without probing them.
    """

    name = "sentinel"
    role = "e-commerce security scanner, investigator and threat intelligence"

    def __init__(self) -> None:
        self.findings: list[SecurityFinding] = []
        self.authorized_targets: set[str] = set()

    def authorize(self, target: str) -> str:
        normalized = self._normalize(target)
        self.authorized_targets.add(normalized)
        return normalized

    def is_authorized(self, target: str) -> bool:
        return self._normalize(target) in self.authorized_targets

    def record_finding(
        self,
        target: str,
        title: str,
        severity: str = "medium",
        evidence: list[str] | None = None,
        verified: bool = False,
        active_test: bool = False,
    ) -> SecurityFinding:
        normalized = self._normalize(target)
        if active_test and normalized not in self.authorized_targets:
            raise PermissionError("active security testing requires an authorized target")
        finding = SecurityFinding(
            target=normalized,
            title=title,
            severity=severity,
            status="verified" if verified else "candidate",
            evidence=evidence or [],
            verified=verified,
        )
        self.findings.append(finding)
        return finding

    def create_opportunity(self, finding: SecurityFinding) -> dict[str, Any]:
        return {
            "type": "security_opportunity",
            "target": finding.target,
            "problem": finding.title,
            "severity": finding.severity,
            "verified": finding.verified,
            "evidence": finding.evidence,
            "recommended_service": "e-commerce security assessment and remediation",
            "next": "ORVIA can qualify the prospect and draft a non-binding outreach message",
        }

    def status(self) -> dict[str, Any]:
        return {
            "agent": self.name,
            "role": self.role,
            "authorized_targets": len(self.authorized_targets),
            "findings": len(self.findings),
            "verified_findings": sum(f.verified for f in self.findings),
            "dark_intel": "intelligence-ready; no credential trading or unauthorized access",
        }

    @staticmethod
    def _normalize(target: str) -> str:
        value = target.strip()
        parsed = urlparse(value if "://" in value else f"https://{value}")
        if not parsed.netloc:
            raise ValueError("target must be a valid domain or URL")
        return parsed.netloc.lower().removeprefix("www.")


sentinel = Sentinel()
