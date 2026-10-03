"""
Database layer for Hamed AI Core.

Uses Python's built-in `sqlite3` module ONLY, on purpose:
  - The spec (section 24) lists DATABASE_URL as optional in Core.
  - We still want real persistence out of the box without forcing a
    `pip install` of SQLAlchemy/psycopg2 before the project even boots.
  - Because it is stdlib, this module is trivially portable back to
    Python 3.8 on Windows 7, matching the environment mentioned in the
    original project (spec section 22).

Swapping to Postgres/MySQL for production scale is a drop-in job:
replace this module's connection with any DB-API 2.0 driver, since
all SQL below is plain ANSI-ish SQL and the Repository layer (see
repository.py) is the only thing that talks to it — the rest of the
app never touches SQL directly (spec section 30: separate DB from
Agents/Tools/Channels).
"""
from __future__ import annotations

import os
import sqlite3
import threading
from contextlib import contextmanager

from app.config import settings

_SCHEMA = """
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact TEXT,                  -- phone/email/handle, used for dedup
    source TEXT,
    activity TEXT,
    interest TEXT,
    stage TEXT NOT NULL DEFAULT 'NEW_LEAD',
    score REAL DEFAULT 0,
    expected_value REAL DEFAULT 0,
    last_contact_at TEXT,
    next_followup_at TEXT,
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(contact)
);

CREATE TABLE IF NOT EXISTS opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER,
    source TEXT,
    opp_type TEXT,
    confidence REAL DEFAULT 0,
    opportunity_score REAL DEFAULT 0,
    potential_value REAL DEFAULT 0,
    next_step TEXT,
    discovered_at TEXT NOT NULL,
    FOREIGN KEY (lead_id) REFERENCES leads(id)
);

CREATE TABLE IF NOT EXISTS proposals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER NOT NULL,
    service TEXT,
    price REAL,
    status TEXT NOT NULL DEFAULT 'DRAFT',
    created_at TEXT NOT NULL,
    FOREIGN KEY (lead_id) REFERENCES leads(id)
);

CREATE TABLE IF NOT EXISTS deals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER NOT NULL,
    proposal_id INTEGER,
    status TEXT NOT NULL DEFAULT 'OPEN',       -- OPEN/WON/LOST
    expected_revenue REAL DEFAULT 0,
    actual_revenue REAL DEFAULT 0,
    lost_reason TEXT,
    closed_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (lead_id) REFERENCES leads(id),
    FOREIGN KEY (proposal_id) REFERENCES proposals(id)
);

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'PENDING',    -- PENDING/RUNNING/DONE/FAILED
    scheduled_at TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS agent_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent TEXT NOT NULL,
    task_summary TEXT,
    status TEXT NOT NULL,
    error TEXT,
    started_at TEXT NOT NULL,
    finished_at TEXT
);

CREATE TABLE IF NOT EXISTS permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    auto_allowed INTEGER NOT NULL DEFAULT 0,
    UNIQUE(actor, action)
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    reason TEXT,
    input_data TEXT,
    result TEXT,
    permission TEXT NOT NULL,      -- AUTO / APPROVED / DENIED / PENDING_APPROVAL
    timestamp TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS revenue_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    deal_id INTEGER,
    source TEXT,
    amount REAL NOT NULL,
    kind TEXT NOT NULL,            -- EXPECTED / ACTUAL
    recorded_at TEXT NOT NULL,
    FOREIGN KEY (deal_id) REFERENCES deals(id)
);
"""


class Database:
    """Thread-safe wrapper around a single SQLite connection."""

    def __init__(self, path: str | None = None):
        self.path = path or settings.sqlite_path()
        if self.path != ":memory:":
            directory = os.path.dirname(self.path)
            if directory:
                os.makedirs(directory, exist_ok=True)
        self._local = threading.local()
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        if not hasattr(self._local, "conn"):
            conn = sqlite3.connect(self.path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            self._local.conn = conn
        return self._local.conn

    def _init_schema(self) -> None:
        conn = self._connect()
        conn.executescript(_SCHEMA)
        conn.commit()

    @contextmanager
    def cursor(self):
        conn = self._connect()
        cur = conn.cursor()
        try:
            yield cur
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()

    def close(self) -> None:
        if hasattr(self._local, "conn"):
            self._local.conn.close()
            del self._local.conn


_default_db: Database | None = None


def get_database() -> Database:
    """Process-wide singleton, override in tests by constructing Database directly."""
    global _default_db
    if _default_db is None:
        _default_db = Database()
    return _default_db
