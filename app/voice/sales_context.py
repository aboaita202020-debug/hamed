"""Build a structured pre-call sales brief for Hamed's voice agent."""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class SalesContext:
    customer_name: str = ""
    business_name: str = ""
    website: str = ""
    observed_problems: tuple[str, ...] = field(default_factory=tuple)
    likely_needs: tuple[str, ...] = field(default_factory=tuple)
    recommended_services: tuple[str, ...] = field(default_factory=tuple)
    target_price: float | None = None
    minimum_price: float | None = None
    objective: str = "discovery"

    def as_prompt(self) -> str:
        lines = [
            "PRE-CALL SALES BRIEF:",
            f"Customer: {self.customer_name or 'unknown'}",
            f"Business: {self.business_name or 'unknown'}",
            f"Website: {self.website or 'unknown'}",
            f"Observed problems: {', '.join(self.observed_problems) or 'none verified'}",
            f"Likely needs: {', '.join(self.likely_needs) or 'discover during call'}",
            f"Recommended services: {', '.join(self.recommended_services) or 'discover during call'}",
            f"Objective: {self.objective}",
        ]
        if self.target_price is not None:
            lines.append(f"Target price: {self.target_price}")
        if self.minimum_price is not None:
            lines.append(f"Minimum price: {self.minimum_price}")
        lines.append("Use only verified facts from this brief. Never invent missing customer information.")
        return "\n".join(lines)
