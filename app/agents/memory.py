"""Lightweight persistent memory for Hamed sessions and decisions."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


class AgentMemory:
    def __init__(self, path: str = "data/hamed_memory.sqlite3") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT NOT NULL, kind TEXT NOT NULL, payload TEXT NOT NULL, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)")
            db.commit()

    def remember(self, session_id: str, kind: str, payload: dict[str, Any]) -> None:
        with sqlite3.connect(self.path) as db:
            db.execute("INSERT INTO memories(session_id, kind, payload) VALUES (?, ?, ?)", (session_id, kind, json.dumps(payload, ensure_ascii=False)))
            db.commit()

    def recent(self, session_id: str, limit: int = 20) -> list[dict[str, Any]]:
        with sqlite3.connect(self.path) as db:
            rows = db.execute("SELECT kind, payload, created_at FROM memories WHERE session_id=? ORDER BY id DESC LIMIT ?", (session_id, limit)).fetchall()
        return [{"kind": kind, "payload": json.loads(payload), "created_at": created_at} for kind, payload, created_at in reversed(rows)]
