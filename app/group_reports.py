from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

from .agents import DEPARTMENT_COUNTS

REPORT_HEADERS = [
    "generated_at", "period", "department", "agent_count", "agents_participating",
    "completed", "discoveries", "learning", "errors", "collaboration", "alerts",
    "active_work", "next_actions", "details"
]


def _sheets_config() -> dict[str, str | bool]:
    return {
        "enabled": os.getenv("ORVIA_GOOGLE_SHEETS_ENABLED", "false").lower() in {"1", "true", "yes"},
        "spreadsheet_id": os.getenv("ORVIA_GOOGLE_SHEETS_SPREADSHEET_ID", ""),
        "credentials_file": os.getenv("GOOGLE_APPLICATION_CREDENTIALS", ""),
    }


def _sheets_append(row: list[Any]) -> dict[str, Any]:
    cfg = _sheets_config()
    if not cfg["enabled"]:
        return {"status": "disabled", "reason": "ORVIA_GOOGLE_SHEETS_ENABLED is false"}
    try:
        import gspread  # type: ignore
        from google.oauth2.service_account import Credentials  # type: ignore

        if not cfg["spreadsheet_id"] or not cfg["credentials_file"]:
            return {"status": "not_configured", "reason": "spreadsheet id or credentials file missing"}
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
        ]
        creds = Credentials.from_service_account_file(str(cfg["credentials_file"]), scopes=scopes)
        client = gspread.authorize(creds)
        book = client.open_by_key(str(cfg["spreadsheet_id"]))
        worksheet = book.worksheet("ORVIA Reports")
        worksheet.append_row([str(x) for x in row], value_input_option="USER_ENTERED")
        return {"status": "saved", "spreadsheet_id": cfg["spreadsheet_id"], "worksheet": "ORVIA Reports"}
    except Exception as exc:  # noqa: BLE001 - external Sheets API boundary
        return {"status": "error", "error": str(exc)}


def group_report(department: str, *, period: str = "daily", events: dict[str, Any] | None = None) -> dict[str, Any]:
    events = events or {}
    now = datetime.now(timezone.utc).isoformat()
    agent_count = int(DEPARTMENT_COUNTS.get(department, 0))
    report = {
        "generated_at": now,
        "period": period,
        "department": department,
        "agent_count": agent_count,
        "agents_participating": int(events.get("agents_participating", agent_count)),
        "completed": events.get("completed", []),
        "discoveries": events.get("discoveries", []),
        "learning": events.get("learning", []),
        "errors": events.get("errors", []),
        "collaboration": events.get("collaboration", []),
        "alerts": events.get("alerts", []),
        "active_work": events.get("active_work", []),
        "next_actions": events.get("next_actions", []),
        "details": events.get("details", {}),
    }
    return report


def all_group_reports(period: str = "daily", events_by_department: dict[str, dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    events_by_department = events_by_department or {}
    return [group_report(dept, period=period, events=events_by_department.get(dept)) for dept in DEPARTMENT_COUNTS]


def save_group_reports(reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results = []
    for report in reports:
        row = [
            report["generated_at"], report["period"], report["department"], report["agent_count"],
            report["agents_participating"], json.dumps(report["completed"], ensure_ascii=False),
            json.dumps(report["discoveries"], ensure_ascii=False), json.dumps(report["learning"], ensure_ascii=False),
            json.dumps(report["errors"], ensure_ascii=False), json.dumps(report["collaboration"], ensure_ascii=False),
            json.dumps(report["alerts"], ensure_ascii=False), json.dumps(report["active_work"], ensure_ascii=False),
            json.dumps(report["next_actions"], ensure_ascii=False), json.dumps(report["details"], ensure_ascii=False),
        ]
        results.append({"department": report["department"], **_sheets_append(row)})
    return results


def reports_status() -> dict[str, Any]:
    cfg = _sheets_config()
    return {
        "google_sheets": {
            "enabled": bool(cfg["enabled"]),
            "configured": bool(cfg["spreadsheet_id"] and cfg["credentials_file"]),
            "worksheet": "ORVIA Reports",
            "required_env": ["ORVIA_GOOGLE_SHEETS_ENABLED", "ORVIA_GOOGLE_SHEETS_SPREADSHEET_ID", "GOOGLE_APPLICATION_CREDENTIALS"],
        },
        "departments": {k: v for k, v in DEPARTMENT_COUNTS.items()},
    }
