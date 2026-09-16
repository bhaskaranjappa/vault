"""File-backed memory store implementing remember/update/invalidate/conflict.

Storage layout (under a root directory, default 11_STATE/memory):
  index.yaml          - retrieval index (YAML-compatible, implementation state)
  records/MEM-*.json  - one JSON record per durable memory
  conflicts/CONFLICT-*.json - explicit conflict records
  checkpoints/CHK-*.json    - logical task checkpoints
  context_packages/CTX-*.json - context packages

This store is operational state only; it is never canonical project truth.
"""

from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

from .records import MemoryRecord, utc_now, new_memory_id


class MemoryStore:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.records_dir = self.root / "records"
        self.conflicts_dir = self.root / "conflicts"
        self.checkpoints_dir = self.root / "checkpoints"
        self.ctx_dir = self.root / "context_packages"
        for d in (self.records_dir, self.conflicts_dir,
                  self.checkpoints_dir, self.ctx_dir):
            d.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ paths
    def _record_path(self, memory_id: str) -> Path:
        return self.records_dir / f"{memory_id}.json"

    # ------------------------------------------------------------- operations
    def remember(self, record: MemoryRecord) -> MemoryRecord:
        record.validate()
        if self._record_path(record.memory_id).exists():
            raise ValueError(f"memory_id already exists: {record.memory_id}")
        record.created_at = record.created_at or utc_now()
        record.updated_at = record.created_at
        self._write_record(record)
        return record

    def get(self, memory_id: str) -> Optional[MemoryRecord]:
        path = self._record_path(memory_id)
        if not path.exists():
            return None
        return MemoryRecord.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def all_records(self) -> list[MemoryRecord]:
        out = []
        for path in sorted(self.records_dir.glob("MEM-*.json")):
            out.append(MemoryRecord.from_dict(json.loads(path.read_text(encoding="utf-8"))))
        return out

    def update(self, memory_id: str, new_content: str, *,
               source_kind: str, source_ref: str,
               classification: str = "STATED",
               conflict: bool = False,
               **field_updates) -> tuple[MemoryRecord, MemoryRecord]:
        """Supersede a memory with a new current record.

        The old record is preserved and marked SUPERSEDED (or CONFLICTING when
        ``conflict=True``); the new record carries fresh provenance and links
        back via related_memories. Never silently destroys history.
        """
        old = self.get(memory_id)
        if old is None:
            raise KeyError(f"unknown memory_id: {memory_id}")
        old.status = "CONFLICTING" if conflict else "SUPERSEDED"
        old.updated_at = utc_now()
        if memory_id not in old.related_memories:
            pass  # old record keeps its own history of relations
        self._write_record(old)

        new = MemoryRecord(
            content=new_content,
            type=field_updates.pop("type", old.type),
            classification=classification,
            source_kind=source_kind,
            source_ref=source_ref,
            confidence=field_updates.pop("confidence", old.confidence),
            project=field_updates.pop("project", old.project),
            task=field_updates.pop("task", old.task),
            tags=field_updates.pop("tags", list(old.tags)),
            sensitivity=field_updates.pop("sensitivity", old.sensitivity),
            related_memories=[memory_id],
            conflict_refs=[memory_id] if conflict else list(old.conflict_refs),
        )
        new.validate()
        new.created_at = utc_now()
        new.updated_at = new.created_at
        self._write_record(new)
        if conflict:
            self.record_conflict(old.memory_id, new.memory_id)
        return old, new

    def invalidate(self, memory_id: str, reason: str = "") -> MemoryRecord:
        rec = self.get(memory_id)
        if rec is None:
            raise KeyError(f"unknown memory_id: {memory_id}")
        rec.status = "INVALIDATED"
        rec.updated_at = utc_now()
        if reason:
            rec.tags = sorted(set(rec.tags) | {f"invalidated:{reason}"})
        self._write_record(rec)
        return rec

    def record_conflict(self, id_a: str, id_b: str) -> str:
        conflict_id = "CONFLICT-" + uuid.uuid4().hex[:10]
        (self.conflicts_dir / f"{conflict_id}.json").write_text(
            json.dumps({
                "conflict_id": conflict_id,
                "memories": [id_a, id_b],
                "created_at": utc_now(),
            }, indent=2),
            encoding="utf-8")
        other = {id_a: id_b, id_b: id_a}
        for mid, other_id in other.items():
            rec = self.get(mid)
            if rec is None:
                continue
            if rec.status == "ACTIVE":
                rec.status = "CONFLICTING"
            if other_id not in rec.conflict_refs:
                rec.conflict_refs.append(other_id)
            rec.updated_at = utc_now()
            self._write_record(rec)
        return conflict_id

    def list_conflicts(self) -> list[dict]:
        return [json.loads(p.read_text(encoding="utf-8"))
                for p in sorted(self.conflicts_dir.glob("CONFLICT-*.json"))]

    # -------------------------------------------------------------- internals
    def _write_record(self, rec: MemoryRecord) -> None:
        self._record_path(rec.memory_id).write_text(
            json.dumps(rec.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8")
        self._write_index()

    def _write_index(self) -> None:
        records = self.all_records()
        lines = [
            "version: 1",
            "description: PAIOS durable-memory retrieval index; implementation state only, not canonical project knowledge.",
            f"last_updated: {utc_now()}",
            "records:",
        ]
        for r in records:
            lines.append(f"  - {r.memory_id}")
        lines.append("conflicts:")
        for c in self.list_conflicts():
            lines.append(f"  - {c['conflict_id']}")
        (self.root / "index.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")
