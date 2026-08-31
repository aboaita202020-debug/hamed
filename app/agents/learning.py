"""Continuous knowledge ingestion for Hamed.

Sources are connectors, not hard-coded content. The learner stores source
metadata, extracted knowledge and provenance, then asks specialist agents to
review and reconcile it. It does not silently rewrite production policy or
permissions from untrusted material.
"""
from __future__ import annotations

import hashlib
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class KnowledgeItem:
    source: str
    title: str
    content: str
    url: str | None = None
    trust: str = "unverified"


class KnowledgeBase:
    def __init__(self, path: str = "data/hamed_knowledge.sqlite3") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS knowledge (id INTEGER PRIMARY KEY AUTOINCREMENT, fingerprint TEXT UNIQUE, source TEXT, title TEXT, content TEXT, url TEXT, trust TEXT, created_at TEXT)")
            db.commit()

    def ingest(self, item: KnowledgeItem) -> bool:
        fingerprint = hashlib.sha256((item.source + "\n" + item.title + "\n" + item.content).encode("utf-8")).hexdigest()
        with sqlite3.connect(self.path) as db:
            cur = db.execute("INSERT OR IGNORE INTO knowledge(fingerprint, source, title, content, url, trust, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)", (fingerprint, item.source, item.title, item.content, item.url, item.trust, datetime.now(timezone.utc).isoformat()))
            db.commit()
            return cur.rowcount == 1

    def ingest_many(self, items: Iterable[KnowledgeItem]) -> int:
        return sum(self.ingest(item) for item in items)

    def search(self, query: str, limit: int = 10) -> list[KnowledgeItem]:
        terms = [term for term in query.lower().split() if term]
        if not terms:
            return []
        clauses = " OR ".join(["lower(title) LIKE ? OR lower(content) LIKE ?" for _ in terms])
        args = [arg for term in terms for arg in (f"%{term}%", f"%{term}%")]
        with sqlite3.connect(self.path) as db:
            rows = db.execute(f"SELECT source,title,content,url,trust FROM knowledge WHERE {clauses} ORDER BY id DESC LIMIT ?", (*args, limit)).fetchall()
        return [KnowledgeItem(*row) for row in rows]


DEFAULT_SOURCE_CLASSES = (
    "official_docs", "books", "academic_papers", "websites", "news", "industry_reports",
    "public_datasets", "github", "user_files", "connected_apps", "customer_feedback",
    "internal_logs", "agent_results",
)


def learning_policy() -> dict[str, object]:
    return {
        "source_classes": list(DEFAULT_SOURCE_CLASSES),
        "learn_continuously": True,
        "preserve_provenance": True,
        "deduplicate": True,
        "require_verification_for_high_impact_facts": True,
        "never_learn_permissions_or_secrets_from_content": True,
        "never_treat_unverified_content_as_fact": True,
    }
