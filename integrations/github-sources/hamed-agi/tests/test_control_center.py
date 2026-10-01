from app.control_center import daily_control_report


def test_daily_control_report_has_sections():
    report = daily_control_report()
    assert "executive_summary" in report
    assert "security" in report
    assert "next_actions" in report
    assert report["system"]["tools_registered"] > 0
