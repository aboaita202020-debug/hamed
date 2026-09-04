"""Plain dataclasses mirroring the SQL schema in database.py.

Kept dependency-free (no ORM) so Core has zero third-party requirements.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


# --- Pipeline stages (spec section 7) ---------------------------------
PIPELINE_STAGES = [
    "NEW_LEAD",
    "RESEARCHED",
    "QUALIFIED",
    "CONTACTED",
    "ENGAGED",
    "PROPOSAL",
    "NEGOTIATION",
    "WON",
    "LOST",
    "ONBOARDING",
    "FOLLOW_UP",
]


@dataclass
class Lead:
    id: Optional[int] = None
    name: str = ""
    contact: str = ""
    source: str = ""
    activity: str = ""
    interest: str = ""
    stage: str = "NEW_LEAD"
    score: float = 0.0
    expected_value: float = 0.0
    last_contact_at: Optional[str] = None
    next_followup_at: Optional[str] = None
    notes: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @staticmethod
    def from_row(row) -> "Lead":
        return Lead(**{k: row[k] for k in row.keys()})


@dataclass
class Opportunity:
    id: Optional[int] = None
    lead_id: Optional[int] = None
    source: str = ""
    opp_type: str = ""
    confidence: float = 0.0
    opportunity_score: float = 0.0
    potential_value: float = 0.0
    next_step: str = ""
    discovered_at: Optional[str] = None

    @staticmethod
    def from_row(row) -> "Opportunity":
        return Opportunity(**{k: row[k] for k in row.keys()})


@dataclass
class Proposal:
    id: Optional[int] = None
    lead_id: int = 0
    service: str = ""
    price: float = 0.0
    status: str = "DRAFT"
    created_at: Optional[str] = None

    @staticmethod
    def from_row(row) -> "Proposal":
        return Proposal(**{k: row[k] for k in row.keys()})


@dataclass
class Deal:
    id: Optional[int] = None
    lead_id: int = 0
    proposal_id: Optional[int] = None
    status: str = "OPEN"
    expected_revenue: float = 0.0
    actual_revenue: float = 0.0
    lost_reason: Optional[str] = None
    closed_at: Optional[str] = None
    created_at: Optional[str] = None

    @staticmethod
    def from_row(row) -> "Deal":
        return Deal(**{k: row[k] for k in row.keys()})


@dataclass
class AuditLogEntry:
    actor: str
    action: str
    permission: str  # AUTO / APPROVED / DENIED / PENDING_APPROVAL
    reason: str = ""
    input_data: str = ""
    result: str = ""
    timestamp: Optional[str] = None
    id: Optional[int] = None
