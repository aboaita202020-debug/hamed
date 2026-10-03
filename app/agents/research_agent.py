"""Commercial research specialist using the configured AI provider's web tool."""
from dataclasses import dataclass
from .provider import AIProvider


@dataclass(frozen=True)
class ResearchReport:
    query: str
    findings: str


class ResearchAgent:
    def __init__(self, provider: AIProvider) -> None:
        self.provider = provider

    def research(self, query: str) -> ResearchReport:
        if not query.strip():
            raise ValueError("Research query cannot be empty")
        findings = self.provider.web_research(query)
        return ResearchReport(query=query, findings=findings)
