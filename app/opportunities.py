from .models import Opportunity


def score_opportunity(problem: str, evidence: list[str], expected_value: float = 0.0) -> Opportunity:
    evidence_score = min(len(evidence) / 3, 1.0)
    value_score = min(max(expected_value, 0.0) / 10000, 1.0)
    score = round(0.65 * evidence_score + 0.35 * value_score, 3)
    return Opportunity(
        title="Evidence-backed commercial opportunity",
        problem=problem,
        solution="Design a measurable service or experiment around the verified problem.",
        evidence=evidence,
        score=score,
        reversible=True,
        requires_approval=False,
    )
