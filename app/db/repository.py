"""
Repository = the ONLY place in the codebase allowed to write SQL.
Agents and Tools call this layer, never the Database class directly
(spec section 30: separate Agents from Database).

Implements:
  - CRM (create/update/find leads) with Deduplication by `contact`.
  - Opportunity, Proposal, Deal persistence.
  - Audit Log for every important action (spec section 13).
  - Revenue events (Expected vs Actual, spec section 20).
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Optional

from .database import Database
from .models import Lead, Opportunity, Proposal, Deal, AuditLogEntry


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Repository:
    def __init__(self, db: Database):
        self.db = db

    # ------------------------------------------------------------------
    # CRM / Leads  (spec section 14 + Deduplication requirement)
    # ------------------------------------------------------------------
    def upsert_lead(
        self,
        name: str,
        contact: str,
        source: str = "",
        activity: str = "",
        interest: str = "",
        stage: str = "NEW_LEAD",
        score: float = 0.0,
        expected_value: float = 0.0,
        notes: str = "",
    ) -> Lead:
        """Create a lead, or update the existing one if `contact` already
        exists — this IS the deduplication rule required by the spec."""
        existing = self.find_lead_by_contact(contact) if contact else None
        contact_value = contact if contact else None  # NULL, so SQLite's
        # UNIQUE constraint treats each contact-less lead as distinct
        # instead of colliding on an empty string.
        now = _now()
        with self.db.cursor() as cur:
            if existing:
                cur.execute(
                    """UPDATE leads SET name=?, source=?, activity=?, interest=?,
                       stage=?, score=?, expected_value=?, notes=?, updated_at=?
                       WHERE id=?""",
                    (name or existing.name, source or existing.source,
                     activity or existing.activity, interest or existing.interest,
                     stage or existing.stage, score or existing.score,
                     expected_value or existing.expected_value,
                     notes or existing.notes, now, existing.id),
                )
                return self.get_lead(existing.id)
            cur.execute(
                """INSERT INTO leads
                   (name, contact, source, activity, interest, stage, score,
                    expected_value, notes, created_at, updated_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (name, contact_value, source, activity, interest, stage, score,
                 expected_value, notes, now, now),
            )
            new_id = cur.lastrowid
        return self.get_lead(new_id)

    def find_lead_by_contact(self, contact: str) -> Optional[Lead]:
        if not contact:
            return None
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM leads WHERE contact = ?", (contact,))
            row = cur.fetchone()
        return Lead.from_row(row) if row else None

    def get_lead(self, lead_id: int) -> Optional[Lead]:
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
            row = cur.fetchone()
        return Lead.from_row(row) if row else None

    def update_lead_stage(self, lead_id: int, stage: str) -> None:
        with self.db.cursor() as cur:
            cur.execute(
                "UPDATE leads SET stage=?, updated_at=? WHERE id=?",
                (stage, _now(), lead_id),
            )

    def list_leads(self, stage: Optional[str] = None) -> list[Lead]:
        with self.db.cursor() as cur:
            if stage:
                cur.execute("SELECT * FROM leads WHERE stage=? ORDER BY updated_at DESC", (stage,))
            else:
                cur.execute("SELECT * FROM leads ORDER BY updated_at DESC")
            rows = cur.fetchall()
        return [Lead.from_row(r) for r in rows]

    # ------------------------------------------------------------------
    # Opportunities (spec section 6)
    # ------------------------------------------------------------------
    def add_opportunity(self, opp: Opportunity) -> Opportunity:
        with self.db.cursor() as cur:
            cur.execute(
                """INSERT INTO opportunities
                   (lead_id, source, opp_type, confidence, opportunity_score,
                    potential_value, next_step, discovered_at)
                   VALUES (?,?,?,?,?,?,?,?)""",
                (opp.lead_id, opp.source, opp.opp_type, opp.confidence,
                 opp.opportunity_score, opp.potential_value, opp.next_step, _now()),
            )
            opp.id = cur.lastrowid
        return opp

    def list_opportunities(self, min_score: float = 0.0) -> list[Opportunity]:
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT * FROM opportunities WHERE opportunity_score >= ? "
                "ORDER BY opportunity_score DESC",
                (min_score,),
            )
            rows = cur.fetchall()
        return [Opportunity.from_row(r) for r in rows]

    # ------------------------------------------------------------------
    # Proposals / Deals (spec section 7 & 20)
    # ------------------------------------------------------------------
    def add_proposal(self, proposal: Proposal) -> Proposal:
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO proposals (lead_id, service, price, status, created_at) "
                "VALUES (?,?,?,?,?)",
                (proposal.lead_id, proposal.service, proposal.price,
                 proposal.status, _now()),
            )
            proposal.id = cur.lastrowid
        return proposal

    def open_deal(self, lead_id: int, proposal_id: Optional[int], expected_revenue: float) -> Deal:
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO deals (lead_id, proposal_id, status, expected_revenue, created_at) "
                "VALUES (?,?,?,?,?)",
                (lead_id, proposal_id, "OPEN", expected_revenue, _now()),
            )
            deal_id = cur.lastrowid
        self.record_revenue_event(deal_id, "pipeline", expected_revenue, "EXPECTED")
        return self.get_deal(deal_id)

    def get_deal(self, deal_id: int) -> Optional[Deal]:
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM deals WHERE id=?", (deal_id,))
            row = cur.fetchone()
        return Deal.from_row(row) if row else None

    def close_deal(self, deal_id: int, won: bool, actual_revenue: float = 0.0,
                    lost_reason: Optional[str] = None) -> Deal:
        status = "WON" if won else "LOST"
        with self.db.cursor() as cur:
            cur.execute(
                "UPDATE deals SET status=?, actual_revenue=?, lost_reason=?, closed_at=? WHERE id=?",
                (status, actual_revenue, lost_reason, _now(), deal_id),
            )
        if won and actual_revenue:
            self.record_revenue_event(deal_id, "closed_deal", actual_revenue, "ACTUAL")
        return self.get_deal(deal_id)

    def pipeline_metrics(self) -> dict[str, Any]:
        with self.db.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS c FROM deals")
            total = cur.fetchone()["c"]
            cur.execute("SELECT COUNT(*) AS c FROM deals WHERE status='WON'")
            won = cur.fetchone()["c"]
            cur.execute("SELECT COALESCE(SUM(expected_revenue),0) AS s FROM deals WHERE status='OPEN'")
            expected = cur.fetchone()["s"]
            cur.execute("SELECT COALESCE(SUM(actual_revenue),0) AS s FROM deals WHERE status='WON'")
            actual = cur.fetchone()["s"]
        close_rate = (won / total * 100) if total else 0.0
        return {
            "total_deals": total,
            "won_deals": won,
            "close_rate_pct": round(close_rate, 2),
            "expected_revenue": expected,
            "actual_revenue": actual,
        }

    # ------------------------------------------------------------------
    # Revenue events (Expected vs Actual, spec section 5 & 20)
    # ------------------------------------------------------------------
    def record_revenue_event(self, deal_id: Optional[int], source: str, amount: float, kind: str) -> None:
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO revenue_events (deal_id, source, amount, kind, recorded_at) "
                "VALUES (?,?,?,?,?)",
                (deal_id, source, amount, kind, _now()),
            )

    # ------------------------------------------------------------------
    # Audit Log (spec section 13: every important action is logged)
    # ------------------------------------------------------------------
    def write_audit_log(self, entry: AuditLogEntry) -> AuditLogEntry:
        with self.db.cursor() as cur:
            cur.execute(
                """INSERT INTO audit_logs (actor, action, reason, input_data, result, permission, timestamp)
                   VALUES (?,?,?,?,?,?,?)""",
                (entry.actor, entry.action, entry.reason,
                 _safe_json(entry.input_data), _safe_json(entry.result),
                 entry.permission, _now()),
            )
            entry.id = cur.lastrowid
        return entry

    def list_audit_logs(self, limit: int = 100) -> list[dict]:
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,))
            rows = cur.fetchall()
        return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # Agent runs (observability, spec section 19)
    # ------------------------------------------------------------------
    def start_agent_run(self, agent: str, task_summary: str) -> int:
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO agent_runs (agent, task_summary, status, started_at) VALUES (?,?,?,?)",
                (agent, task_summary, "RUNNING", _now()),
            )
            return cur.lastrowid

    def finish_agent_run(self, run_id: int, status: str, error: str = "") -> None:
        with self.db.cursor() as cur:
            cur.execute(
                "UPDATE agent_runs SET status=?, error=?, finished_at=? WHERE id=?",
                (status, error, _now(), run_id),
            )

    def dashboard_snapshot(self) -> dict[str, Any]:
        with self.db.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS c FROM leads")
            leads = cur.fetchone()["c"]
            cur.execute("SELECT COUNT(*) AS c FROM opportunities")
            opps = cur.fetchone()["c"]
            cur.execute("SELECT COUNT(*) AS c FROM agent_runs WHERE status='FAILED'")
            errors = cur.fetchone()["c"]
        return {
            "leads": leads,
            "opportunities": opps,
            "agent_errors": errors,
            "pipeline": self.pipeline_metrics(),
        }


def _safe_json(value: Any) -> str:
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, ensure_ascii=False, default=str)
    except TypeError:
        return str(value)
