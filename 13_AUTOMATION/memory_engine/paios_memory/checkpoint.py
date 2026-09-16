"""Logical task checkpoints per 11_STATE/AIOS_CHECKPOINT_SCHEMA_V1.md.

This is logical checkpoint/restore: durable task state on disk. It does NOT
provide filesystem snapshots, transaction rollback, or process restoration.
"""

from __future__ import annotations

import json
import subprocess
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .records import utc_now


@dataclass
class Checkpoint:
    task_id: str
    objective: str
    scope: str = ""
    acceptance_criteria: list = field(default_factory=list)
    completed: list = field(default_factory=list)      # {action, status, evidence}
    current_state: dict = field(default_factory=dict)  # {phase, active_action, observations}
    decisions: list = field(default_factory=list)      # {decision, rationale, evidence}
    blockers: list = field(default_factory=list)
    next_actions: list = field(default_factory=list)
    context_package: Optional[str] = None
    authority_scope: str = "task-scoped"
    workers: list = field(default_factory=list)        # {worker_id, role, state, result_ref}
    evidence_refs: list = field(default_factory=list)
    conflicts: list = field(default_factory=list)
    risks: list = field(default_factory=list)
    repository: dict = field(default_factory=dict)
    checkpoint_id: str = field(default_factory=lambda: "CHK-" + uuid.uuid4().hex[:10])
    version: int = 1
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "checkpoint_id": self.checkpoint_id,
            "task_id": self.task_id,
            "version": self.version,
            "created_at": self.created_at or utc_now(),
            "updated_at": self.updated_at or utc_now(),
            "repository": self.repository,
            "objective": self.objective,
            "scope": self.scope,
            "acceptance_criteria": self.acceptance_criteria,
            "completed": self.completed,
            "current_state": self.current_state,
            "decisions": self.decisions,
            "blockers": self.blockers,
            "next_actions": self.next_actions,
            "context_package": self.context_package,
            "authority_scope": self.authority_scope,
            "workers": self.workers,
            "evidence_refs": self.evidence_refs,
            "conflicts": self.conflicts,
            "risks": self.risks,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Checkpoint":
        return cls(
            checkpoint_id=d["checkpoint_id"],
            task_id=d["task_id"],
            version=d.get("version", 1),
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"),
            repository=d.get("repository", {}),
            objective=d["objective"],
            scope=d.get("scope", ""),
            acceptance_criteria=list(d.get("acceptance_criteria", [])),
            completed=list(d.get("completed", [])),
            current_state=dict(d.get("current_state", {})),
            decisions=list(d.get("decisions", [])),
            blockers=list(d.get("blockers", [])),
            next_actions=list(d.get("next_actions", [])),
            context_package=d.get("context_package"),
            authority_scope=d.get("authority_scope", "task-scoped"),
            workers=list(d.get("workers", [])),
            evidence_refs=list(d.get("evidence_refs", [])),
            conflicts=list(d.get("conflicts", [])),
            risks=list(d.get("risks", [])),
        )


def repo_state(repo_path: str | Path = ".") -> dict:
    """Capture lightweight git state for checkpoint consistency checks."""
    def git(*args: str) -> str:
        try:
            out = subprocess.run(["git", *args], cwd=repo_path,
                                 capture_output=True, text=True, timeout=15)
            return out.stdout.strip() if out.returncode == 0 else "UNKNOWN"
        except Exception:
            return "UNKNOWN"
    head = git("rev-parse", "HEAD")
    status = git("status", "--porcelain")
    return {
        "ref": "git",
        "branch": git("rev-parse", "--abbrev-ref", "HEAD") or "UNKNOWN",
        "head": head or "UNKNOWN",
        "working_tree": "CLEAN" if status == "" else "DIRTY" if status != "UNKNOWN" else "UNKNOWN",
    }


class CheckpointStore:
    def __init__(self, root: str | Path, repo_path: str | Path = "."):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.repo_path = Path(repo_path)

    def _path(self, checkpoint_id: str) -> Path:
        return self.root / f"{checkpoint_id}.json"

    def create_checkpoint(self, chk: Checkpoint) -> Checkpoint:
        if chk.repository == {}:
            chk.repository = repo_state(self.repo_path)
        chk.created_at = chk.created_at or utc_now()
        chk.updated_at = chk.created_at
        self._write(chk)
        return chk

    def update_checkpoint(self, checkpoint_id: str, **updates) -> Checkpoint:
        chk = self.load_checkpoint(checkpoint_id)
        for key, value in updates.items():
            if not hasattr(chk, key):
                raise KeyError(f"unknown checkpoint field: {key}")
            setattr(chk, key, value)
        chk.updated_at = utc_now()
        chk.repository = repo_state(self.repo_path)
        self._write(chk)
        return chk

    def load_checkpoint(self, checkpoint_id: str) -> Checkpoint:
        path = self._path(checkpoint_id)
        if not path.exists():
            raise FileNotFoundError(f"checkpoint not found: {checkpoint_id}")
        return Checkpoint.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def _write(self, chk: Checkpoint) -> None:
        self._path(chk.checkpoint_id).write_text(
            json.dumps(chk.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8")


def resume(store: CheckpointStore, checkpoint_id: str, *,
           expected_authority: str | None = None) -> dict:
    """Safe resume: load -> verify state -> verify authority -> verify claims.

    Returns a report; the caller decides whether to continue. If repository
    state has changed (HEAD moved, or recorded CLEAN/DIRTY mismatch), the
    report flags it instead of blindly continuing.
    """
    chk = store.load_checkpoint(checkpoint_id)
    current = repo_state(store.repo_path)
    discrepancies = []
    if chk.repository.get("head") not in (None, "UNKNOWN") and \
            current["head"] != chk.repository.get("head"):
        discrepancies.append(
            f"HEAD changed since checkpoint: {chk.repository.get('head')[:12]} -> {current['head'][:12]}")
    if chk.repository.get("working_tree") and current["working_tree"] != chk.repository.get("working_tree"):
        discrepancies.append(
            f"working_tree changed: {chk.repository.get('working_tree')} -> {current['working_tree']}")
    authority_ok = expected_authority is None or chk.authority_scope == expected_authority
    unverified_claims = [
        c["action"] for c in chk.completed
        if not c.get("evidence")
    ]
    return {
        "checkpoint": chk,
        "current_repository": current,
        "discrepancies": discrepancies,
        "authority_ok": authority_ok,
        "unverified_completed_claims": unverified_claims,
        "next_action": chk.next_actions[0] if chk.next_actions else None,
        "safe_to_continue": not discrepancies and authority_ok,
    }
