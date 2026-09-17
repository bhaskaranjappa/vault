"""AutomationEngine facade (prompt §3 pipeline).

Automation Intent -> Trigger -> Context Loader -> Authority Check
-> Phase 10 Route -> Phase 9 Task/Worker -> Executor Adapter
-> Result Verification -> Acceptance Check -> Run Record
-> Checkpoint / Recovery

Every layer is a separate component; the engine only orchestrates the
contract. Untrusted content is data and can never change scope or authority.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .automation import (
    AuthorityDecision, AuthorityVerifier, AutomationIntent, AutomationLedger,
    AutomationState, ConditionRegistry, ConditionEvaluation, ExecutorAdapter,
    ExecutionResult, InvalidAutomationTransition, InlineNoOpAdapter, RunRecord,
    Trigger, TriggerType, now_iso,
)
from .events import AutomationEventLog

INJECTION_MARKERS = (
    "ignore previous instructions", "ignore paios policy", "disable safeguards",
    "grant yourself", "expand your scope", "you are now", "authorize yourself",
    "override policy",
)


class UntrustedContent(Exception):
    """Retrieved content attempted to exercise authority over the engine."""


class DuplicateRunBlocked(Exception):
    """An idempotency-equivalent run already exists for the execution window."""


class AutomationEngine:
    def __init__(self, state_root: str | Path, *,
                 executor: ExecutorAdapter | None = None,
                 authority: AuthorityVerifier | None = None,
                 conditions: ConditionRegistry | None = None):
        self.root = Path(state_root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.ledger = AutomationLedger(self.root)
        self.events = AutomationEventLog(self.root)
        self.executor = executor                    # None => control-plane only
        self.authority = authority or AuthorityVerifier()
        self.conditions = conditions or ConditionRegistry()

    # -- untrusted content ---------------------------------------------------
    def ingest_retrieved_content(self, text: str, source: str) -> dict:
        lowered = (text or "").lower()
        hits = [m for m in INJECTION_MARKERS if m in lowered]
        if hits:
            self.events.log("REJECTED", automation_id="SYSTEM",
                            payload={"kind": "untrusted_content", "source": source,
                                     "markers": hits})
            raise UntrustedContent(
                f"content from {source} attempted to instruct the automation engine "
                f"({hits}); recorded as untrusted data and refused")
        return {"accepted": True, "source": source}

    # -- lifecycle ------------------------------------------------------------
    def create_automation(self, **fields) -> AutomationIntent:
        fields.setdefault("automation_id", AutomationIntent.new_id())
        aut = AutomationIntent(**fields)
        self.ledger.save_automation(aut)
        self.events.log("AUTOMATION_CREATED", automation_id=aut.automation_id,
                        payload={"objective": aut.objective, "trigger": aut.trigger.trigger_type})
        return aut

    def enable(self, automation_id: str, *, actor: str = "owner-policy") -> AutomationIntent:
        aut = self.ledger.load_automation(automation_id)
        # High-impact / irreversible activation gate (AU-05, AU-18).
        result = self.authority.verify(aut, action="activate")
        if result.decision != AuthorityDecision.AUTHORIZED:
            self.events.log("REJECTED", automation_id=automation_id,
                            payload={"reason": result.reason})
            raise PermissionError(f"activation blocked: {result.reason}")
        aut.transition(AutomationState.ENABLED, reason=f"enabled by {actor}")
        aut.enabled = True
        self.ledger.save_automation(aut)
        self.events.log("AUTOMATION_ENABLED", automation_id=automation_id,
                        payload={"actor": actor})
        return aut

    def disable(self, automation_id: str, *, reason: str = "") -> AutomationIntent:
        aut = self.ledger.load_automation(automation_id)
        if aut.state == AutomationState.RUNNING:
            # in-flight cancellation is runtime-dependent (Protocol §10): the
            # control plane can only mark the automation disabled-for-new-runs
            # after the run reaches a terminal state.
            raise InvalidAutomationTransition(
                "in-flight run cannot be disabled portably; cancel via the "
                "runtime adapter, then disable")
        aut.transition(AutomationState.DISABLED, reason=reason or "disabled")
        aut.enabled = False
        self.ledger.save_automation(aut)
        self.events.log("AUTOMATION_DISABLED", automation_id=automation_id,
                        payload={"reason": reason})
        return aut

    # -- triggers ---------------------------------------------------------------
    def trigger_matches(self, automation: AutomationIntent, *,
                        manual: bool = False, event_name: str | None = None,
                        now: str | None = None) -> bool:
        """Logical trigger match. Actual scheduling is an adapter concern."""
        t = automation.trigger
        if automation.state not in (AutomationState.ENABLED,):
            return False
        if t.trigger_type == TriggerType.MANUAL:
            return bool(manual)
        if t.trigger_type == TriggerType.EVENT:
            return bool(event_name and event_name == t.event_name)
        if t.trigger_type in (TriggerType.SCHEDULED, TriggerType.RECURRING):
            # schedule metadata is validated/persisted; firing is adapter-driven
            return bool(manual)      # adapter may inject a manual firing
        if t.trigger_type == TriggerType.CONDITION:
            return self.conditions.evaluate(t.condition).value == "TRUE"
        return False

    # -- idempotency ------------------------------------------------------------
    def _check_idempotency(self, aut: AutomationIntent) -> None:
        token = aut.idempotency_token()
        for run in self.ledger.runs_for(aut.automation_id):
            if run.idempotency_token == token and \
                    run.result in ("COMPLETED", "UNKNOWN", "RECONCILE", "PENDING"):
                raise DuplicateRunBlocked(
                    f"run {run.run_id} already covers idempotency token "
                    f"({token}) with result {run.result}; duplicate external action prevented")

    # -- run lifecycle -------------------------------------------------------------
    def start_run(self, automation_id: str, *, manual: bool = False,
                  event_name: str | None = None, now: str | None = None) -> RunRecord:
        aut = self.ledger.load_automation(automation_id)
        if aut.state == AutomationState.DISABLED:
            self.events.log("REJECTED", automation_id=automation_id,
                            payload={"reason": "automation is DISABLED"})
            raise PermissionError(f"automation {automation_id} is DISABLED; no new runs")
        if aut.state == AutomationState.SUCCEEDED:
            aut.transition(AutomationState.ENABLED, reason="re-arm for repeatable trigger")
            self.ledger.save_automation(aut)
        if not self.trigger_matches(aut, manual=manual, event_name=event_name, now=now):
            # recognize a duplicate trigger of an in-flight run explicitly
            try:
                self._check_idempotency(aut)
            except DuplicateRunBlocked:
                raise
            raise PermissionError(f"trigger does not match automation {automation_id}")
        self._check_idempotency(aut)

        # authority check before execution (AU-04)
        auth = self.authority.verify(aut, action="execute")
        self.events.log("AUTHORITY_CHECKED", automation_id=automation_id,
                        payload={"decision": auth.decision, "reason": auth.reason})
        if auth.decision != AuthorityDecision.AUTHORIZED:
            raise PermissionError(f"run blocked by authority: {auth.reason}")

        aut.transition(AutomationState.RUNNING, reason="trigger matched")
        self.ledger.save_automation(aut)

        run = RunRecord(
            run_id=RunRecord.new_id(), automation_id=automation_id,
            trigger_type=aut.trigger.trigger_type, started_at=now or now_iso(),
            executor=self.executor.adapter_id if self.executor else "none",
            authority_scope=aut.authority_scope, authority_decision=auth.decision,
            context_package_id=aut.context_package_id,
            idempotency_token=aut.idempotency_token())
        self.ledger.save_run(run)
        self.events.log("RUN_STARTED", automation_id=automation_id, run_id=run.run_id,
                        payload={"trigger": run.trigger_type})
        return run

    def record_route(self, run_id: str, route_ref: str) -> RunRecord:
        run = self.ledger.load_run(run_id)
        run.route_ref = route_ref
        self.ledger.save_run(run)
        self.events.log("ROUTE_SELECTED", automation_id=run.automation_id,
                        run_id=run_id, payload={"route_ref": route_ref})
        return run

    def execute(self, run_id: str) -> ExecutionResult:
        run = self.ledger.load_run(run_id)
        aut = self.ledger.load_automation(run.automation_id)
        if self.executor is None:
            result = ExecutionResult(status="COMPLETED",
                                     detail="no executor configured; control-plane only")
        else:
            self.events.log("WORK_STARTED", automation_id=run.automation_id, run_id=run_id)
            result = self.executor.execute(aut, run)
        run.actions_attempted.append({"adapter": run.executor, "status": result.status,
                                      "detail": result.detail})
        run.result = result.status
        if result.status == "FAILED":
            run.error = result.error or result.detail
        self.ledger.save_run(run)
        if result.status == "COMPLETED":
            self.events.log("WORK_COMPLETED", automation_id=run.automation_id, run_id=run_id)
        return result

    def verify(self, run_id: str) -> dict:
        run = self.ledger.load_run(run_id)
        self.events.log("VERIFY_STARTED", automation_id=run.automation_id, run_id=run_id)
        if run.result == "UNKNOWN":
            self.events.log("VERIFY_FAILED", automation_id=run.automation_id, run_id=run_id,
                            payload={"reason": "unknown execution state requires reconciliation"})
            return {"verified": False, "reason": "UNKNOWN result: reconcile before any retry "
                                                 "of duplicate-prone external actions"}
        if run.result == "FAILED":
            self.events.log("VERIFY_FAILED", automation_id=run.automation_id, run_id=run_id,
                            payload={"error": run.error})
            return {"verified": False, "reason": run.error or "execution failed"}
        if self.executor is not None:
            aut = self.ledger.load_automation(run.automation_id)
            verdict = self.executor.verify(aut, run)
            if not verdict.get("verified"):
                self.events.log("VERIFY_FAILED", automation_id=run.automation_id,
                                run_id=run_id, payload=verdict)
                return verdict
            run.verification = verdict
            self.ledger.save_run(run)
        return {"verified": True}

    def evaluate_acceptance(self, run_id: str, *,
                            criterion_evidence: dict | None = None) -> dict:
        """Per-criterion acceptance with explicit evidence. A technically
        completed action with failed criteria must remain failed (AU-11)."""
        run = self.ledger.load_run(run_id)
        aut = self.ledger.load_automation(run.automation_id)
        criterion_evidence = criterion_evidence or {}
        results = {}
        for crit in aut.acceptance_criteria:
            results[crit] = bool(criterion_evidence.get(crit))
        run.acceptance = results
        passed = bool(results) and all(results.values()) and run.result == "COMPLETED"
        self.ledger.save_run(run)
        self.events.log("ACCEPTED" if passed else "REJECTED",
                        automation_id=run.automation_id, run_id=run_id,
                        payload={"acceptance": results})
        return {"passed": passed, "criteria": results}

    def close_run(self, run_id: str, *, evidence_refs: list | None = None) -> RunRecord:
        run = self.ledger.load_run(run_id)
        aut = self.ledger.load_automation(run.automation_id)
        accepted = bool(run.acceptance) and all(run.acceptance.values())
        if accepted and run.result == "COMPLETED":
            run.final_state = "SUCCEEDED"
            run.ended_at = now_iso()
            aut.transition(AutomationState.SUCCEEDED, reason="acceptance passed")
            self.events.log("RUN_SUCCEEDED", automation_id=aut.automation_id,
                            run_id=run_id, payload={"evidence_refs": evidence_refs or []})
        else:
            run.final_state = "FAILED"
            run.ended_at = now_iso()
            aut.transition(AutomationState.FAILED,
                           reason="acceptance failed" if run.result == "COMPLETED"
                                  else (run.error or "execution failed"))
            self.events.log("RUN_FAILED", automation_id=aut.automation_id,
                            run_id=run_id, payload={"result": run.result,
                                                    "acceptance": run.acceptance})
        if evidence_refs:
            run.evidence_refs.extend(evidence_refs)
        self.ledger.save_run(run)
        self.ledger.save_automation(aut)
        return run

    # -- retry / recovery (AU-09/10/15) --------------------------------------------
    def retry(self, run_id: str, *, reason: str) -> RunRecord:
        if not reason:
            raise ValueError("retry requires a concrete recovery reason")
        run = self.ledger.load_run(run_id)
        aut = self.ledger.load_automation(run.automation_id)
        if run.result == "UNKNOWN":
            raise PermissionError(
                "cannot retry an UNKNOWN run; reconcile state first to avoid "
                "duplicating a possibly-completed external action")
        if run.recovery_attempts >= aut.retry_limit:
            raise PermissionError(
                f"retry limit reached ({run.recovery_attempts}/{aut.retry_limit}); terminal failure")
        # A retry never expands authority or scope (AU-09): same run, same token.
        run.recovery_attempts += 1
        run.retry_reasons.append(reason)
        self.ledger.save_run(run)
        aut.transition(AutomationState.RETRYING, reason=reason)
        self.ledger.save_automation(aut)
        self.events.log("RETRY_STARTED", automation_id=aut.automation_id, run_id=run_id,
                        payload={"attempt": run.recovery_attempts, "reason": reason})
        return run

    def reconcile_unknown(self, run_id: str, *, evidence_refs: list) -> RunRecord:
        """Explicit reconciliation of an UNKNOWN run (AU-10 / AD-08): preserve
        evidence and surface an unresolved state; never silently retry."""
        run = self.ledger.load_run(run_id)
        run.result = "RECONCILE"
        run.evidence_refs.extend(evidence_refs)
        self.ledger.save_run(run)
        self.events.log("VERIFY_FAILED", automation_id=run.automation_id, run_id=run_id,
                        payload={"reconciled": True, "evidence_refs": evidence_refs})
        return run

    # -- restart recovery (AU-07 / prompt §22) --------------------------------------
    def recover_after_restart(self, automation_id: str) -> dict:
        """Load automation + latest run; verify state; identify the next safe
        action. A stale or uncertain run is NEVER blindly resumed."""
        aut = self.ledger.load_automation(automation_id)
        runs = self.ledger.runs_for(automation_id)
        latest = runs[-1] if runs else None
        if latest is None:
            return {"automation": aut.state, "next_action": "none: no runs",
                    "safe": True}
        if latest.final_state == "RUNNING":
            # stale in-flight run: requires reconciliation, not resumption
            latest.result = "RECONCILE"
            self.ledger.save_run(latest)
            return {"automation": aut.state, "run": latest.run_id,
                    "next_action": "reconcile stale RUNNING run before any retry",
                    "safe": False, "checkpoint_id": latest.checkpoint_id}
        return {"automation": aut.state, "run": latest.run_id,
                "final_state": latest.final_state,
                "next_action": "create a new run" if aut.state == AutomationState.ENABLED
                               else "none", "safe": True}
