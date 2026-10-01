from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any


class MemoryStore:
    def __init__(self, path: str = "data/orvia_memory.jsonl") -> None:
        self.path = Path(path)
        self._lock = Lock()
    def record(self, kind: str, data: dict[str, Any], source: str = "system") -> dict[str, Any]:
        item = {"timestamp": datetime.now(timezone.utc).isoformat(), "kind": kind, "source": source, "data": data}
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(item, ensure_ascii=False) + "\n")
        return item
    def recent(self, limit: int = 50) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as fh:
            lines = fh.readlines()[-max(1, min(limit, 500)):]
        result = []
        for line in lines:
            try:
                result.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return result

memory_store = MemoryStore()
