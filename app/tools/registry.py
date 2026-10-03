"""Controlled allow-list for Hamed tools."""

class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, name, handler, risk="low", read_only=True):
        if name in self._tools:
            raise ValueError("Tool already registered: " + name)
        self._tools[name] = {"handler": handler, "risk": risk, "read_only": read_only}

    def names(self):
        return sorted(self._tools.keys())

    def execute(self, name, approved=False, **kwargs):
        tool = self._tools.get(name)
        if tool is None:
            raise KeyError("Unknown tool: " + name)
        if tool["risk"] == "high" and not approved:
            raise PermissionError("Approval required for tool: " + name)
        return tool["handler"](**kwargs)
