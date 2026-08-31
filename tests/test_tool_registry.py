import pytest

from app.agents.tool_registry import ToolRegistry, ToolSpec


def test_registry_registers_and_returns_scoped_tool():
    registry = ToolRegistry()
    handler = lambda value: value + 1
    registry.register(
        ToolSpec(
            name="calculator",
            description="Calculate a bounded expression",
            handler=handler,
            required_permission="calculator:read",
        )
    )

    tool = registry.get("calculator")
    assert tool.handler(4) == 5
    assert tool.read_only is True


def test_registry_rejects_duplicate_tools():
    registry = ToolRegistry()
    spec = ToolSpec("x", "x", lambda: None, "x:read")
    registry.register(spec)

    with pytest.raises(ValueError, match="already registered"):
        registry.register(spec)


def test_registry_rejects_unknown_tools():
    registry = ToolRegistry()

    with pytest.raises(KeyError, match="Unknown Hamed tool"):
        registry.get("missing")
