import pytest

from app.agents.central_brain import CentralBrainProvider


class FakeBrain:
    def __init__(self, value="council"):
        self.value = value
        self.calls = 0

    def generate_response(self, messages, *, system=""):
        self.calls += 1
        return self.value

    def web_research(self, query, *, system=""):
        self.calls += 1
        return self.value

    def available_brains(self):
        return ("fake",)


def test_central_brain_prefers_openai():
    provider = CentralBrainProvider(None)
    provider.central = FakeBrain("openai")
    provider.council = FakeBrain("council")
    assert provider.generate_response([{"role": "user", "content": "hello"}]) == "openai"
    assert provider.central.calls == 1
    assert provider.council.calls == 0


def test_central_brain_falls_back_to_council():
    class BrokenBrain(FakeBrain):
        def generate_response(self, messages, *, system=""):
            self.calls += 1
            raise RuntimeError("down")

    provider = CentralBrainProvider(None)
    provider.central = BrokenBrain()
    provider.council = FakeBrain("council")
    assert provider.generate_response([{"role": "user", "content": "hello"}]) == "council"
    assert provider.central.calls == 1
    assert provider.council.calls == 1


def test_central_brain_reports_mode_and_brains():
    provider = CentralBrainProvider(None)
    provider.central = FakeBrain("openai")
    provider.council = None
    assert provider.mode == "openai-central"
    assert provider.available_brains() == ["openai-central"]
