"""Safety and commercial policy helpers for outbound Hamed calls."""
from dataclasses import dataclass


@dataclass(frozen=True)
class CallPolicy:
    disclose_ai: bool = True
    require_explicit_consent_for_recording: bool = True
    max_attempts_per_number: int = 1
    allow_high_impact_commitments: bool = False


def validate_outbound_target(phone_number: str, allowlist: set[str]) -> None:
    if phone_number not in allowlist:
        raise ValueError("Phone number is not on the approved outbound allowlist")


def validate_attempt_count(attempts: int, policy: CallPolicy) -> None:
    if attempts >= policy.max_attempts_per_number:
        raise ValueError("Outbound attempt limit reached for this number")
