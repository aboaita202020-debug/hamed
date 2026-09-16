from app.agents.autopilot import build_autopilot_plan, classify_goal


def test_classify_commercial_domains():
    assert classify_goal("ابحث عن فرص تسويق بالعمولة") == "affiliate"
    assert classify_goal("اعمل متجر إلكتروني") == "website"
    assert classify_goal("ابحث عن مورد منتج لإعادة البيع") == "commerce"
    assert classify_goal("هات عملاء لخدمة تصميم مواقع") == "services"
    assert classify_goal("اعمل حملة تسويق") == "marketing"


def test_autopilot_plan_keeps_consequential_actions_gated():
    plan = build_autopilot_plan("ابحث عن منتج مربح لإعادة البيع")
    assert "supplier_research" in plan.pipeline
    assert "purchase" in plan.approval_steps
    assert "payment" in plan.approval_steps
    assert "contract" in plan.approval_steps
    assert "irreversible" in plan.approval_steps
