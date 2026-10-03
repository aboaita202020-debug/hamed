from __future__ import annotations
from pathlib import Path

CATALOG = Path(__file__).with_name("free_ai_tools_250.catalog")

def load_specialist_tools():
    tools = []
    for line in CATALOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "|" not in line:
            continue
        category, raw = line.split("|", 1)
        for tool_id in (x.strip() for x in raw.split(",")):
            if not tool_id:
                continue
            tools.append({
                "id": "free-" + tool_id,
                "name": tool_id.replace("_", " ").title(),
                "category": category,
                "capabilities": (tool_id, category),
                "integration": "free-specialist",
                "env_key": None,
            })
    if len(tools) < 250:
        raise RuntimeError(f"Expected at least 250 specialist tools, got {len(tools)}")
    return tuple(tools[:250])

FREE_SPECIALIST_TOOLS = load_specialist_tools()
