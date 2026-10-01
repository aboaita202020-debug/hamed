from app.sentinel import Sentinel


def test_sentinel_requires_authorization_for_active_testing():
    s = Sentinel()
    try:
        s.record_finding("https://shop.example", "test", active_test=True)
        assert False, "expected authorization gate"
    except PermissionError:
        pass


def test_sentinel_creates_security_opportunity():
    s = Sentinel()
    target = s.authorize("https://shop.example")
    finding = s.record_finding(
        target,
        "API authorization weakness",
        severity="high",
        evidence=["publicly documented test evidence"],
        verified=True,
        active_test=True,
    )
    opportunity = s.create_opportunity(finding)
    assert opportunity["type"] == "security_opportunity"
    assert opportunity["verified"] is True
    assert opportunity["target"] == "shop.example"
