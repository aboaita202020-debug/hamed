from app.agents.brain_council import BRAIN_ROLES, BrainCouncil


class FakeProvider:
    def generate_response(self, messages, *, system=""):
        return "ANALYSIS: test\nCONFIDENCE: 90\nRISKS: test risk\nRECOMMENDATION: proceed"


def test_council_has_15_roles():
    assert len(BRAIN_ROLES) == 15
    assert BRAIN_ROLES[-1].name == "ceo_final_judge"


def test_council_deliberates_and_judges():
    result = BrainCouncil(FakeProvider()).deliberate("Evaluate a business opportunity")
    assert result["brains_consulted"] == 14
    assert result["total_brains"] == 15
    assert result["final_judgment"]
    assert len(result["opinions"]) == 14
