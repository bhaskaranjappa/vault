"""Append-only JSONL evidence/event log (prompt §18)."""

from __future__ import annotations

import json
from pathlib import Path
from threading import Lock


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class EventLog:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()

    def log(self, subject_id: str, event_type: str, old_state, new_state,
            *, reason: str = "", evidence_ref=None, extra: dict | None = None) -> dict:
        entry = {
            "timestamp": _now(),
            "subject_id": subject_id,
            "event_type": event_type,
            "old_state": old_state,
            "new_state": new_state,
            "reason": reason,
            "evidence_ref": evidence_ref,
        }
        if extra:
            entry.update(extra)
        with self._lock:
            with self.path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return entry

    def entries(self, subject_id: str | None = None) -> list:
        if not self.path.exists():
            return []
        out = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            e = json.loads(line)
            if subject_id is None or e.get("subject_id") == subject_id:
                out.append(e)
        return out
