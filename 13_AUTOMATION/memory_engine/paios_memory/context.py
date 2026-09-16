"""Context package builder implementing 03_PROTOCOLS/AIOS_CONTEXT_PACKAGE_SCHEMA_V1.md.

Context is selected, not dumped. Selection priority (context budgeting):
  mandatory policy -> task contract -> current state/checkpoint ->
  task-relevant canonical knowledge -> relevant memory -> supporting history

Never drops mission.objective, mandatory policy, or acceptance criteria first.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .records import utc_now, SENSITIVITY_ORDER
from .retrieval import Retriever, RetrievalQuery

INHERITANCE_MODES = ("NONE", "SELECTED", "RECENT_RELEVANT", "FULL")

# Priority tiers for budgeting: lower number = dropped last.
PRIORITY = {
    "policy": 0,
    "mission": 0,
    "acceptance_criteria": 0,
    "state": 1,
    "checkpoint": 1,
    "canonical_files": 2,
    "workflow_refs": 2,
    "memory": 3,
    "history": 4,
}


@dataclass
class TaskSpec:
    task_id: str
    objective: str
    scope: str = ""
    acceptance_criteria: list = field(default_factory=list)


@dataclass
class ContextRequest:
    task: TaskSpec
    canonical_rules: list = field(default_factory=list)      # mandatory policy refs
    canonical_files: list = field(default_factory=list)      # relevant knowledge paths
    workflow_refs: list = field(default_factory=list)
    prohibited_actions: list = field(default_factory=list)
    authority_scope: str = "task-scoped"
    adapter: str = "unknown"
    executor: str = "unknown"
    model_provider: str = "unknown"
    completed: list = field(default_factory=list)
    pending: list = field(default_factory=list)
    blockers: list = field(default_factory=list)
    decisions: list = field(default_factory=list)
    evidence_required: list = field(default_factory=list)
    evidence_refs: list = field(default_factory=list)
    inheritance_mode: str = "SELECTED"
    parent_context_refs: list = field(default_factory=list)
    selected_memory_ids: list = field(default_factory=list)  # SELECTED mode
    max_sensitivity: str = "INTERNAL"
    max_items: Optional[int] = None
    max_chars: Optional[int] = None
    source_checkpoint: Optional[str] = None
    retriever: Optional[Retriever] = None
    retrieval_query: Optional[RetrievalQuery] = None         # RECENT_RELEVANT mode


class ContextBuilder:
    def __init__(self, store_root: str | Path):
        self.ctx_dir = Path(store_root) / "context_packages"
        self.ctx_dir.mkdir(parents=True, exist_ok=True)

    def build(self, req: ContextRequest) -> dict:
        if req.inheritance_mode not in INHERITANCE_MODES:
            raise ValueError(f"invalid inheritance mode: {req.inheritance_mode}")

        # --- memory selection per inheritance mode -------------------------
        selected: list[dict] = []
        excluded: list[str] = []
        if req.inheritance_mode == "SELECTED":
            if req.retriever is not None:
                for mid in req.selected_memory_ids:
                    rec = req.retriever.store.get(mid)
                    if rec is None:
                        raise KeyError(f"selected memory not found: {mid}")
                    if SENSITIVITY_ORDER[rec.sensitivity] > SENSITIVITY_ORDER[req.max_sensitivity]:
                        excluded.append(mid)
                        continue
                    selected.append({"memory_id": mid, "priority": "memory",
                                     "content": rec.content})
        elif req.inheritance_mode in ("RECENT_RELEVANT", "FULL") and req.retriever is not None:
            q = req.retrieval_query or RetrievalQuery(
                text=req.task.objective, task=req.task.task_id,
                max_sensitivity=req.max_sensitivity)
            q.max_sensitivity = req.max_sensitivity
            for sm in req.retriever.retrieve(q):
                selected.append({"memory_id": sm.record.memory_id,
                                 "priority": "memory",
                                 "content": sm.record.content})

        # --- assemble package ----------------------------------------------
        pkg = {
            "context_package_id": "CTX-" + uuid.uuid4().hex[:10],
            "task_id": req.task.task_id,
            "created_at": utc_now(),
            "source_checkpoint": req.source_checkpoint,
            "mission": {
                "objective": req.task.objective,
                "scope": req.task.scope,
                "acceptance_criteria": list(req.task.acceptance_criteria),
            },
            "policy": {
                "canonical_rules": list(req.canonical_rules),
                "authority_scope": req.authority_scope,
                "prohibited_actions": list(req.prohibited_actions),
            },
            "knowledge": {
                "selected_records": selected,
                "canonical_files": list(req.canonical_files),
                "workflow_refs": list(req.workflow_refs),
            },
            "runtime": {
                "adapter": req.adapter,
                "executor": req.executor,
                "model_provider": req.model_provider,
            },
            "state": {
                "completed": list(req.completed),
                "pending": list(req.pending),
                "blockers": list(req.blockers),
                "decisions": list(req.decisions),
            },
            "evidence": {
                "required": list(req.evidence_required),
                "existing_refs": list(req.evidence_refs),
            },
            "inheritance": {
                "mode": req.inheritance_mode,
                "parent_context_refs": list(req.parent_context_refs),
                "excluded_refs": excluded,
            },
            "budget": {
                "max_items": req.max_items,
                "max_tokens": None,
                "max_chars": req.max_chars,
            },
            "sensitivity": {"allowed": _allowed_levels(req.max_sensitivity)},
        }
        self._apply_budget(pkg, req)
        self.ctx_dir / (pkg["context_package_id"] + ".json")
        (self.ctx_dir / f"{pkg['context_package_id']}.json").write_text(
            json.dumps(pkg, indent=2, ensure_ascii=False), encoding="utf-8")
        return pkg

    @staticmethod
    def _apply_budget(pkg: dict, req: ContextRequest) -> None:
        """Truncate lower-priority material first; never drop policy/mission."""
        items = pkg["knowledge"]["selected_records"]
        if req.max_items is not None and len(items) > req.max_items:
            pkg["knowledge"]["selected_records"] = items[:req.max_items]
            pkg["inheritance"]["excluded_refs"].extend(
                i["memory_id"] for i in items[req.max_items:])
            items = pkg["knowledge"]["selected_records"]
        if req.max_chars is not None:
            fixed = _fixed_size(pkg)  # policy + mission + state are protected
            room = req.max_chars - fixed
            kept, kept_ids = [], set()
            for item in items:  # already ordered by selection priority
                cost = len(item["content"]) + len(item["memory_id"]) + 8
                if cost <= room:
                    kept.append(item)
                    room -= cost
                else:
                    kept_ids.add(item["memory_id"])
            pkg["inheritance"]["excluded_refs"].extend(
                i["memory_id"] for i in items if i["memory_id"] in kept_ids)
            pkg["knowledge"]["selected_records"] = kept


def _fixed_size(pkg: dict) -> int:
    protected = {
        "mission": pkg["mission"],
        "policy": pkg["policy"],
        "state": pkg["state"],
        "evidence": pkg["evidence"],
        "runtime": pkg["runtime"],
        "inheritance": pkg["inheritance"],
        "budget": pkg["budget"],
        "sensitivity": pkg["sensitivity"],
        "context_package_id": pkg["context_package_id"],
        "task_id": pkg["task_id"],
        "created_at": pkg["created_at"],
        "source_checkpoint": pkg["source_checkpoint"],
        "canonical_files": pkg["knowledge"]["canonical_files"],
        "workflow_refs": pkg["knowledge"]["workflow_refs"],
    }
    return len(json.dumps(protected, ensure_ascii=False))


def load_context_package(store_root: str | Path, package_id: str) -> dict:
    path = Path(store_root) / "context_packages" / f"{package_id}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _allowed_levels(max_sensitivity: str) -> list:
    idx = SENSITIVITY_ORDER[max_sensitivity]
    return list(SENSITIVITY_ORDER.keys())[:idx + 1]
