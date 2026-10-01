import pytest

from app.tooling import SafetyGovernor, ToolRegistry, ToolSpec


def test_authorization_gate():
    governor = SafetyGovernor()
    tool = ToolSpec("scan", "security", "authorized scan", requires_authorization=True)
    with pytest.raises(PermissionError):
        governor.check(tool, authorized=False, dry_run=False)
    governor.check(tool, authorized=True, dry_run=False)


def test_destructive_tool_is_blocked():
    governor = SafetyGovernor()
    tool = ToolSpec("delete", "system", "delete data", destructive=True)
    with pytest.raises(PermissionError):
        governor.check(tool)


def test_registry_lists_tools():
    registry = ToolRegistry()
    registry.register(ToolSpec("research", "research", "public research"))
    assert registry.list()[0]["name"] == "research"
