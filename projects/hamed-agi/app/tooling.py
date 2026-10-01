from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolSpec:
    name: str
    category: str
    description: str
    requires_authorization: bool = False
    destructive: bool = False


class SafetyGovernor:
    """Central policy gate: active security is scope-controlled; destructive actions stay blocked."""

    def check(self, tool: ToolSpec, *, authorized: bool = False, dry_run: bool = True) -> None:
        if tool.destructive:
            raise PermissionError("destructive actions are blocked by the default safety policy")
        if tool.requires_authorization and not authorized:
            raise PermissionError("this tool requires an explicitly authorized target")


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}
        self._handlers: dict[str, Callable[..., Any]] = {}

    def register(self, spec: ToolSpec, handler: Callable[..., Any] | None = None) -> None:
        self._tools[spec.name] = spec
        if handler is not None:
            self._handlers[spec.name] = handler

    def list(self) -> list[dict[str, Any]]:
        return [self._tools[name].__dict__ for name in sorted(self._tools)]

    def execute(self, name: str, *, authorized: bool = False, dry_run: bool = True, **kwargs: Any) -> dict[str, Any]:
        spec = self._tools.get(name)
        if spec is None:
            raise KeyError(f"unknown tool: {name}")
        SafetyGovernor().check(spec, authorized=authorized, dry_run=dry_run)
        if dry_run:
            return {"status": "planned", "tool": name, "dry_run": True, "message": "dry-run: handler not executed"}
        handler = self._handlers.get(name)
        if handler is None:
            return {"status": "ready", "tool": name, "dry_run": False, "message": "tool registered; handler not installed"}
        return {"status": "ok", "tool": name, "result": handler(dry_run=False, **kwargs)}


def _public_research(*, dry_run: bool = True, target: str | None = None, **_: Any) -> dict[str, Any]:
    if not target:
        return {"status": "skipped", "reason": "target_required"}
    from .research import research
    evidence = research.fetch(target)
    return {"target": target, "evidence": evidence.__dict__}


def _ecommerce_analyzer(*, dry_run: bool = True, target: str | None = None, research_result: dict[str, Any] | None = None, **_: Any) -> dict[str, Any]:
    evidence = (research_result or {}).get("evidence", {})
    return {
        "target": target,
        "signals": {
            "reachable": bool(evidence.get("status_code")),
            "title": evidence.get("title", ""),
            "https": str(target or "").startswith("https://"),
        },
        "mode": "public-analysis",
    }


def _seo_analyzer(*, dry_run: bool = True, target: str | None = None, **_: Any) -> dict[str, Any]:
    return {"target": target, "mode": "public-seo-analysis", "status": "ready"}


def _performance_analyzer(*, dry_run: bool = True, target: str | None = None, **_: Any) -> dict[str, Any]:
    return {"target": target, "mode": "public-performance-analysis", "status": "ready"}


def _opportunity_engine(*, dry_run: bool = True, **_: Any) -> dict[str, Any]:
    from .models import Mission
    from .opportunity import opportunity_engine
    return {"opportunities": [x.model_dump() for x in opportunity_engine.discover(Mission(objective="execution loop"))]}


def _verification(*, dry_run: bool = True, **_: Any) -> dict[str, Any]:
    return {"status": "verified-at-pipeline-level", "note": "promotion still requires evidence-backed verification"}


def _report_generator(*, dry_run: bool = True, **_: Any) -> dict[str, Any]:
    from .control_center import daily_control_report
    return daily_control_report()


def _crm(*, dry_run: bool = True, target: str | None = None, **_: Any) -> dict[str, Any]:
    from .crm import crm
    return {"summary": crm.summary(), "target": target}


def _proposal_generator(*, dry_run: bool = True, **_: Any) -> dict[str, Any]:
    return {"status": "draft-only", "message": "non-binding proposal generation is available after evidence collection"}


def _authorized_sentinel(*, dry_run: bool = True, target: str | None = None, **_: Any) -> dict[str, Any]:
    if not target:
        raise PermissionError("authorized security assessment requires a target")
    from .sentinel import sentinel
    if not sentinel.is_authorized(target):
        raise PermissionError("target is not present in ORVIA Sentinel authorization scope")
    return {"status": "authorized", "target": target, "mode": "safe-assessment", "dry_run": dry_run}


tool_registry = ToolRegistry()

_DEFAULT_TOOLS = [
    (ToolSpec("web_research", "research", "Collect public web evidence"), _public_research),
    (ToolSpec("ecommerce_analyzer", "commerce", "Analyze public e-commerce signals"), _ecommerce_analyzer),
    (ToolSpec("seo_analyzer", "commerce", "Analyze public SEO signals"), _seo_analyzer),
    (ToolSpec("performance_analyzer", "commerce", "Analyze public performance signals"), _performance_analyzer),
    (ToolSpec("threat_intelligence", "security", "Correlate public threat intelligence"), None),
    (ToolSpec("sentinel_authorized_scan", "security", "Run an authorized security assessment", requires_authorization=True), _authorized_sentinel),
    (ToolSpec("code_security", "security", "Analyze code with configured static-security tools"), None),
    (ToolSpec("dependency_security", "security", "Analyze dependencies and packages"), None),
    (ToolSpec("container_security", "security", "Analyze container images/configuration"), None),
    (ToolSpec("secrets_detection", "security", "Detect exposed secrets in authorized code"), None),
    (ToolSpec("cloud_security", "security", "Assess authorized cloud configuration"), None),
    (ToolSpec("api_security", "security", "Assess authorized APIs", requires_authorization=True), None),
    (ToolSpec("crm", "business", "Record and qualify customer relationships"), _crm),
    (ToolSpec("opportunity_engine", "business", "Turn evidence into commercial opportunities"), _opportunity_engine),
    (ToolSpec("proposal_generator", "business", "Draft proposals and service offers"), _proposal_generator),
    (ToolSpec("report_generator", "operations", "Generate daily operational reports"), _report_generator),
    (ToolSpec("learning", "intelligence", "Store feedback and learning signals"), None),
    (ToolSpec("verification", "quality", "Verify findings before promotion"), _verification),
]

for _spec, _handler in _DEFAULT_TOOLS:
    tool_registry.register(_spec, _handler)
