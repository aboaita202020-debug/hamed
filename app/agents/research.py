"""Commercial research specialist backed by the configured AI provider's web search."""
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
        findings = self.provider.web_research(
            query,
            system=(
                "You are Hamed's commercial research specialist. Search the web for current, "
                "relevant supplier/product/market information. Prefer primary sources and "
                "credible marketplaces or manufacturer pages. Return concise findings with "
                "source URLs, prices/currencies when explicitly stated, MOQ, availability, "
                "and important caveats. Never invent missing values. Clearly label estimates."
            ),
        )
        return ResearchReport(query=query, findings=findings)
