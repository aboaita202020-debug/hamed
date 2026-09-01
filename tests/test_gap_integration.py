import os
from app.agents.provider import BrainSelector, MultiBrainProvider
from app.services.safety import AutonomyPolicy, Critic, OutreachPolicy
from app.payments.provider import PaymentProvider, PaymentStatus, VodafoneCashProvider, PaymobProvider


def test_brain_selector_ranks_only_available_brains():
    ranked = BrainSelector().rank("python code", ["openai", "deepseek", "claude"])
    assert ranked[0] == "deepseek"
    assert set(ranked) == {"openai", "deepseek", "claude"}


def test_ten_brain_configuration_with_fake_credentials(monkeypatch):
    keys = {
        "OPENAI_API_KEY":"fake-openai", "ANTHROPIC_API_KEY":"fake-anthropic", "DEEPSEEK_API_KEY":"fake-deepseek",
        "KIMI_API_KEY":"fake-kimi", "GEMINI_API_KEY":"fake-gemini", "MISTRAL_API_KEY":"fake-mistral",
        "QWEN_API_KEY":"fake-qwen", "XAI_API_KEY":"fake-xai", "LLAMA_API_KEY":"fake-llama", "OPENROUTER_API_KEY":"fake-openrouter",
    }
    for k,v in keys.items(): monkeypatch.setenv(k,v)
    router = MultiBrainProvider()
    assert set(router.available_brains()) == {"openai","claude","deepseek","kimi","gemini","mistral","qwen","grok","llama","openrouter"}


def test_safety_and_outreach_boundaries():
    assert not OutreachPolicy().validate(evidence=[])
    assert not OutreachPolicy().validate(evidence=["public"], opted_out=True)
    assert AutonomyPolicy().allowed("research")
    assert not AutonomyPolicy().allowed("payment")
    assert AutonomyPolicy().allowed("payment", explicit_approval=True)
    assert Critic().review("hello", ["public evidence"])["approved"]
    assert not Critic().review("guaranteed result", ["public evidence"])["approved"]


def test_payment_lifecycle_is_explicit_and_verification_is_not_faked():
    for provider in (PaymentProvider(), VodafoneCashProvider(), PaymobProvider()):
        ref = provider.create(100)
        assert ref.status == PaymentStatus.PENDING
        try:
            provider.verify(ref.reference)
        except NotImplementedError:
            pass
        else:
            if provider.name in {"abstract", "vodafone_cash", "paymob"}:
                raise AssertionError("provider must not claim automatic verification")
