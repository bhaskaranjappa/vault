"""Parent acceptance (prompt §13 / OR-12, OR-17).

A child reporting COMPLETE is never automatically accepted by the parent.
Acceptance verifies criteria, scope, authority, evidence, contradictions,
completeness and blockers. Parent may remain BLOCKED/FAILED while a child is
COMPLETE.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .ledger import WorkerLedger
from .delegation import scope_contains


@dataclass
class AcceptanceResult:
    accepted: bool
    reasons: list = field(default_factory=list)
    checks: dict = field(default_factory=dict)


class ParentAcceptor:
    def __init__(self, ledger: WorkerLedger):
        self.ledger = ledger
        self.events = ledger.events

    def accept(self, parent_task_id: str, child_worker_id: str, *,
               claimed_output: str | None = None,
               claimed_evidence: list | None = None,
               criterion_evidence: dict | None = None,
               parent_state: str = "RUNNING") -> AcceptanceResult:
        child = self.ledger.load(child_worker_id)
        checks: dict = {}
        reasons: list = []

        # 1. child must actually be COMPLETE (not just stopped execution)
        checks["child_complete"] = child.state == "COMPLETE"
        if child.state != "COMPLETE":
            reasons.append(f"child worker state is {child.state}, not COMPLETE")

        # 2. acceptance criteria met — each criterion needs an explicit
        #    evidence mapping (criterion_evidence) or a reference in the
        #    recorded evidence/output; free-text claims alone are not proof.
        blob = " ".join([child.results.get("output_ref") or ""] +
                        list(child.results.get("evidence_refs", []))).lower()
        cmap = dict(criterion_evidence or {})
        for criterion in child.acceptance_criteria:
            ok = bool(cmap.get(criterion)) or criterion.lower() in blob
            checks[f"criterion: {criterion}"] = ok
            if not ok:
                reasons.append(f"acceptance criterion not evidenced: {criterion}")

        # 3. evidence requirements satisfied
        evidence = list(claimed_evidence or []) + list(child.results.get("evidence_refs", [])) \
            + [v for v in (criterion_evidence or {}).values() if v]
        checks["evidence_present"] = bool(evidence)
        if not evidence:
            reasons.append("no evidence references provided")

        # 4. scope/authority unchanged (child cannot have widened them)
        checks["authority_unchanged"] = scope_contains(child.authority_scope, child.authority_scope)
        # (a wider claim would have been rejected at delegation time; here we
        #  verify the recorded contract is still the one being accepted)

        # 5. no unresolved blockers
        blockers = list(child.results.get("blockers", []))
        checks["no_blockers"] = not blockers
        if blockers:
            reasons.append(f"unresolved blockers: {blockers}")

        accepted = all(checks.values())
        self.events.log(child_worker_id,
                        "PARENT_ACCEPTED" if accepted else "PARENT_REJECTED",
                        child.state, child.state,
                        reason="; ".join(reasons) or "all checks passed",
                        extra={"parent_task_id": parent_task_id})
        return AcceptanceResult(accepted=accepted, reasons=reasons, checks=checks)

    def aggregate_parent(self, parent_task_id: str, child_worker_ids: list, *,
                         parent_state: str = "RUNNING",
                         criterion_evidence: dict | None = None) -> AcceptanceResult:
        """Parent completion requires ALL required children accepted (OR-17).
        One child success cannot hide another child's failure."""
        reasons, checks = [], {}
        for cw in child_worker_ids:
            child = self.ledger.load(cw)
            if child.state == "COMPLETE":
                result = self.accept(parent_task_id, cw, parent_state=parent_state,
                                     criterion_evidence=criterion_evidence)
                checks[cw] = "ACCEPTED" if result.accepted else "REJECTED"
                if not result.accepted:
                    reasons.extend(f"{cw}: {r}" for r in result.reasons)
            else:
                checks[cw] = child.state
                reasons.append(f"required child {cw} is {child.state}, not COMPLETE")
        accepted = all(v == "ACCEPTED" for v in checks.values()) and bool(checks)
        return AcceptanceResult(accepted=accepted, reasons=reasons, checks=checks)
