"""Durable automation event log (Protocol §8; prompt §21).

Append-only JSONL: each event carries timestamp, event type, automation/run
IDs and a payload. History is never rewritten.
"""

from __future__ import annotations

import json
from pathlib import Path

EVENT_TYPES = (
    "AUTOMATION_CREATED", "AUTOMATION_ENABLED", "AUTOMATION_DISABLED",
    "RUN_STARTED", "AUTHORITY_CHECKED", "ROUTE_SELECTED", "WORK_STARTED",
    "WORK_COMPLETED", "VERIFY_STARTED", "VERIFY_FAILED", "ACCEPTED",
    "REJECTED", "RETRY_STARTED", "RUN_FAILED", "RUN_SUCCEEDED",
)


class AutomationEventLog:
    def __init__(self, root):
        self.path = Path(root) / "events.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, event_type: str, *, automation_id: str,
            run_id: str | None = None, payload: dict | None = None,
            timestamp: str | None = None) -> dict:
        if event_type not in EVENT_TYPES:
            raise ValueError(f"unknown automation event type: {event_type}")
        from .automation import now_iso
        entry = {
            "timestamp": timestamp or now_iso(),
            "event": event_type,
            "automation_id": automation_id,
            "run_id": run_id,
            "payload": payload or {},
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return entry

    def all(self, automation_id: str | None = None) -> list:
        if not self.path.exists():
            return []
        entries = [json.loads(line) for line in
                   self.path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if automation_id:
            entries = [e for e in entries if e["automation_id"] == automation_id]
        return entries
