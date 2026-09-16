"""PAIOS V1+ Phase 9 orchestration tests — OR-01..OR-20 + adversarial battery.

All state is written to temporary directories; no canonical 11_STATE content
is touched. Run: python -m unittest tests.test_phase9 -v
"""

from __future__ import annotations

import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "memory_engine"))

from paios_orch import (  # noqa: E402
    TaskContract, validate_task_contract, InvalidTransition, STATES,
    WorkerLedger, EventLog, Delegation, delegate, SCOPE_ESCALATION_REJECTED,
    AUTHORITY_ESCALATION_REJECTED, scope_contains, DependencyGraph,
    DependencyCycle, ParallelRunner, Supervisor, SupervisionError,
    ParentAcceptor, Dispatcher, Executor, ExecutorCapabilities,
    InlineExecutor, Orchestrator, PORTABLE_OPERATIONS,
)
from paios_memory.context import ContextBuilder, ContextRequest, TaskSpec  # noqa: E402
from paios_memory.checkpoint import CheckpointStore  # noqa: E402


def make_root():
    return tempfile.mkdtemp(prefix="paios_orch_test_")


def sample_task(**over):
    fields = dict(
        parent_task_id=None, objective="produce a research summary",
        scope="read-only research, no external send",
        allowed_tools=["read_files"], authority_scope="task-scoped read-only",
        constraints=["no external communication"], acceptance_criteria=["summary exists"],
        expected_output="summary document", evidence_requirements=["file ref"],
        inputs=[], context_package=None)
    fields.update(over)
    return TaskContract(task_id=TaskContract.new_id(), created_at="2026-09-16T00:00:00Z", **fields)


class OR01_TaskContract(unittest.TestCase):
    def test_OR01_contract_integrity(self):
        t = sample_task(parent_task_id="TASK-parent0001")
        self.assertEqual(validate_task_contract(t), [])
        d = t.to_dict()
        for k in ("task_id", "parent_task_id", "objective", "scope", "inputs",
                  "allowed_tools", "authority_scope", "constraints",
                  "acceptance_criteria", "expected_output", "evidence_requirements",
                  "context_package"):
            self.assertIn(k, d)
        # identity stable across serialization round-trip
        t2 = TaskContract.from_dict(d)
        self.assertEqual(t2.task_id, t.task_id)
        # incomplete contracts surface defects
        bad = sample_task(acceptance_criteria=[])
        self.assertTrue(any("acceptance_criteria" in x for x in validate_task_contract(bad)))


class OR02_BoundedDelegation(unittest.TestCase):
    def test_OR02_child_scope_narrower(self):
        parent = sample_task()
        dlg = delegate(parent, objective="summarize one file", scope="read-only research",
                       allowed_tools=["read_files"], authority_scope="task-scoped read-only",
                       constraints=["no external communication"],
                       acceptance_criteria=["summary exists"], evidence_requirements=["ref"])
        self.assertTrue(scope_contains(parent.scope, dlg.scope))

    def test_scope_escalation_rejected(self):
        parent = sample_task()
        with self.assertRaises(PermissionError) as cm:
            delegate(parent, objective="x", scope="read-only research, external send",
                     allowed_tools=[], authority_scope="task-scoped read-only",
                     constraints=[], acceptance_criteria=["c"], evidence_requirements=[])
        self.assertEqual(str(cm.exception), SCOPE_ESCALATION_REJECTED)


class OR03_NestedDelegation(unittest.TestCase):
    def test_OR03_hierarchy_and_ancestry(self):
        root = make_root()
        orch = Orchestrator(root)
        t0 = orch.create_task(objective="root objective", scope="read-only research",
                              allowed_tools=["read_files"], authority_scope="task-scoped read-only",
                              constraints=["no external communication"],
                              acceptance_criteria=["done"], expected_output="out",
                              evidence_requirements=["ref"])
        w0 = orch.spawn_worker(t0.task_id, role="coordinator")
        dlg = orch.delegate(t0.task_id, objective="coordinator subtask",
                            scope="read-only research", allowed_tools=["read_files"],
                            authority_scope="task-scoped read-only",
                            constraints=["no external communication"],
                            acceptance_criteria=["done"], evidence_requirements=["ref"],
                            parent_worker_id=w0.worker_id)
        w1 = orch.spawn_delegated_worker(dlg, role="specialist", parent_worker_id=w0.worker_id)
        dlg2 = orch.delegate(dlg.child_task_id, objective="leaf subtask",
                             scope="read-only research", allowed_tools=["read_files"],
                             authority_scope="task-scoped read-only",
                             constraints=["no external communication"],
                             acceptance_criteria=["done"], evidence_requirements=["ref"],
                             parent_worker_id=w1.worker_id)
        w2 = orch.spawn_delegated_worker(dlg2, role="worker", parent_worker_id=w1.worker_id)
        chain = orch.ledger.ancestry(w2.worker_id)
        self.assertEqual([w.worker_id for w in chain], [w2.worker_id, w1.worker_id, w0.worker_id])
        self.assertEqual([w.role for w in chain], ["worker", "specialist", "coordinator"])
        # no descendant can widen authority
        with self.assertRaises(PermissionError):
            orch.delegate(dlg2.child_task_id, objective="x", scope="read-only research, external send",
                          allowed_tools=[], authority_scope="task-scoped read-only",
                          constraints=[], acceptance_criteria=["c"], evidence_requirements=[],
                          parent_worker_id=w2.worker_id)


class OR04_ParallelWorkers(unittest.TestCase):
    def test_OR04_parallel_independent(self):
        runner = ParallelRunner(max_workers=3)
        branches = {
            "a": ("WRK-aaaaaaaaaa", lambda ctx=None: "result-A"),
            "b": ("WRK-bbbbbbbbbb", lambda ctx=None: time.sleep(0.01) or "result-B"),
            "c": ("WRK-cccccccccc", lambda ctx=None: (_ for _ in ()).throw(RuntimeError("boom"))),
        }
        results = runner.run(branches)
        agg = runner.aggregate(results)
        self.assertEqual(agg["total"], 3)
        self.assertEqual(agg["succeeded"], ["a", "b"])
        self.assertEqual(agg["failed"], ["c"])
        self.assertFalse(results["c"].ok)
        self.assertIn("RuntimeError", results["c"].error)


class OR05_Dependencies(unittest.TestCase):
    def test_OR05_dependency_scheduling(self):
        g = DependencyGraph()
        g.declare("C", ["A", "B"])
        states = {"A": "COMPLETE", "B": "RUNNING"}
        self.assertEqual(g.readiness("C", states), "BLOCKED")
        states["B"] = "COMPLETE"
        self.assertEqual(g.readiness("C", states), "READY")
        # failure propagation
        states["B"] = "FAILED"
        self.assertEqual(g.readiness("C", states), "POISONED")
        self.assertIn("dependency failure", g.blocker_for("C", states))
        # cycle rejection
        with self.assertRaises(DependencyCycle):
            g.declare("A", ["C"])

    def test_dependency_violation_via_dispatcher(self):
        g = DependencyGraph()
        g.declare("C", ["A"])
        d = Dispatcher(g)
        decision = d.decide_task("C", {"A": "PENDING"})
        self.assertEqual(decision.action, "WAIT_DEPENDENCY")


class OR06_Lifecycle(unittest.TestCase):
    def test_OR06_transitions(self):
        root = make_root()
        ledger = WorkerLedger(root)
        w = ledger.create(task_id="TASK-x", parent_task_id=None, role="worker",
                          runtime="test", model_provider="unknown", objective="o",
                          scope="s", authority_scope="a", allowed_tools=[],
                          constraints=[], acceptance_criteria=["c"], context_package=None)
        self.assertEqual(w.state, "PENDING")
        ledger.transition(w.worker_id, "RUNNING")
        ledger.transition(w.worker_id, "COMPLETE")
        # terminal COMPLETE accepts nothing further
        with self.assertRaises(InvalidTransition):
            ledger.transition(w.worker_id, "RUNNING")
        # stale-style invalid: PENDING -> COMPLETE skipped through no acceptance
        w2 = ledger.create(task_id="TASK-y", parent_task_id=None, role="worker",
                           runtime="test", model_provider="unknown", objective="o",
                           scope="s", authority_scope="a", allowed_tools=[],
                           constraints=[], acceptance_criteria=["c"], context_package=None)
        with self.assertRaises(InvalidTransition):
            ledger.transition(w2.worker_id, "COMPLETE")
        # stop without acceptance never yields COMPLETE
        ledger.transition(w2.worker_id, "RUNNING")
        ledger.transition(w2.worker_id, "STOPPED")
        self.assertEqual(ledger.load(w2.worker_id).state, "STOPPED")


class OR07_Inspect(unittest.TestCase):
    def test_OR07_inspect(self):
        root = make_root()
        ledger = WorkerLedger(root)
        w = ledger.create(task_id="TASK-i", parent_task_id=None, role="worker",
                          runtime="test", model_provider="unknown", objective="o",
                          scope="s", authority_scope="a", allowed_tools=[],
                          constraints=[], acceptance_criteria=["c"], context_package=None)
        ledger.transition(w.worker_id, "RUNNING", reason="working on step 1")
        sup = Supervisor(ledger)
        info = sup.inspect(w.worker_id)
        self.assertEqual(info["state"], "RUNNING")
        self.assertEqual(info["worker_id"], w.worker_id)
        self.assertIn("step 1", info["progress"]["summary"])


class OR08_Redirect(unittest.TestCase):
    def test_OR08_bounded_redirect(self):
        root = make_root()
        ledger = WorkerLedger(root)
        w = ledger.create(task_id="TASK-r", parent_task_id=None, role="worker",
                          runtime="test", model_provider="unknown", objective="o",
                          scope="s", authority_scope="a", allowed_tools=[],
                          constraints=[], acceptance_criteria=["c"], context_package=None)
        ledger.transition(w.worker_id, "RUNNING")
        sup = Supervisor(ledger)
        sup.redirect(w.worker_id, {"summary": "course corrected", "pending": ["fix x"]})
        info = sup.inspect(w.worker_id)
        self.assertIn("course corrected", info["progress"]["summary"])
        # redirect may not widen authority
        with self.assertRaises(SupervisionError):
            sup.redirect(w.worker_id, {"authority_scope": "global admin"})


class OR09_Resume(unittest.TestCase):
    def test_OR09_resume(self):
        root = make_root()
        ledger = WorkerLedger(root)
        w = ledger.create(task_id="TASK-res", parent_task_id=None, role="worker",
                          runtime="test", model_provider="unknown", objective="o",
                          scope="s", authority_scope="a", allowed_tools=[],
                          constraints=[], acceptance_criteria=["c"], context_package=None)
        ledger.transition(w.worker_id, "RUNNING")
        ledger.transition(w.worker_id, "STOPPED", reason="paused")
        sup = Supervisor(ledger)
        resumed = sup.resume(w.worker_id, reason="continue")
        self.assertEqual(resumed.state, "RUNNING")
        self.assertEqual(resumed.worker_id, w.worker_id)  # identity preserved
        with self.assertRaises(SupervisionError):
            sup.resume(w2id := (ledger.create(
                task_id="TASK-t", parent_task_id=None, role="worker", runtime="t",
                model_provider="u", objective="o", scope="s", authority_scope="a",
                allowed_tools=[], constraints=[], acceptance_criteria=["c"],
                context_package=None)).worker_id)  # PENDING cannot resume


class OR10_StopCancel(unittest.TestCase):
    def test_OR10_stop_cancel(self):
        root = make_root()
        ledger = WorkerLedger(root)
        ids = []
        for i in range(2):
            w = ledger.create(task_id=f"TASK-sc{i}", parent_task_id=None, role="worker",
                              runtime="test", model_provider="unknown", objective="o",
                              scope="s", authority_scope="a", allowed_tools=[],
                              constraints=[], acceptance_criteria=["c"], context_package=None)
            ledger.transition(w.worker_id, "RUNNING")
            ids.append(w.worker_id)
        sup = Supervisor(ledger)
        sup.stop(ids[0], reason="halt")
        sup.cancel(ids[1], reason="abort")
        self.assertEqual(ledger.load(ids[0]).state, "STOPPED")
        self.assertEqual(ledger.load(ids[1]).state, "CANCELLED")
        # terminal states cannot be revived into COMPLETE
        with self.assertRaises(InvalidTransition):
            ledger.transition(ids[1], "COMPLETE")


class OR11_Recovery(unittest.TestCase):
    def test_OR11_failure_recovery(self):
        root = make_root()
        orch = Orchestrator(root)
        t = orch.create_task(objective="o", scope="read-only research",
                             allowed_tools=[], authority_scope="task-scoped read-only",
                             constraints=[], acceptance_criteria=["c"],
                             expected_output="e", evidence_requirements=["r"])
        w = orch.spawn_worker(t.task_id)
        orch.start(w.worker_id)
        orch.fail(w.worker_id, error_type="transient", message="network hiccup")
        rec = orch.ledger.load(w.worker_id)
        self.assertEqual(rec.state, "FAILED")
        self.assertEqual(len(rec.errors), 1)           # evidence preserved
        sup = orch.supervisor
        out = sup.recover(w.worker_id, strategy="retry", reason="transient error")
        self.assertEqual(out["worker"].state, "RUNNING")
        rec2 = orch.ledger.load(w.worker_id)
        self.assertEqual(rec2.recovery["attempts"], 1)
        self.assertEqual(len(rec2.errors), 1)          # original failure never discarded
        self.assertTrue(rec2.errors[0]["message"] == "network hiccup")


class OR12_ParentAcceptance(unittest.TestCase):
    def test_OR12_reject_incomplete_child(self):
        root = make_root()
        orch = Orchestrator(root)
        t = orch.create_task(objective="o", scope="read-only research",
                             allowed_tools=[], authority_scope="task-scoped read-only",
                             constraints=[], acceptance_criteria=["criterion-A satisfied"],
                             expected_output="e", evidence_requirements=["r"])
        w = orch.spawn_worker(t.task_id)
        orch.start(w.worker_id)
        orch.complete(w.worker_id, output_ref="out.txt", evidence_refs=[])  # no criterion evidence
        res = orch.acceptor.accept(t.task_id, w.worker_id,
                                   claimed_output="partial output without criterion-A satisfied",
                                   claimed_evidence=[])
        self.assertFalse(res.accepted)
        self.assertTrue(any("criterion-A" in r for r in res.reasons))
        # now satisfy it
        res2 = orch.acceptor.accept(t.task_id, w.worker_id,
                                    claimed_output="see report",
                                    criterion_evidence={"criterion-A satisfied": "ev-1"})
        self.assertTrue(res2.accepted)


class OR13_EvidenceProvenance(unittest.TestCase):
    def test_OR13_evidence_attached(self):
        root = make_root()
        orch = Orchestrator(root)
        t = orch.create_task(objective="o", scope="read-only research",
                             allowed_tools=[], authority_scope="task-scoped read-only",
                             constraints=[], acceptance_criteria=["criterion-X done"],
                             expected_output="e", evidence_requirements=["r"])
        w = orch.spawn_worker(t.task_id)
        orch.start(w.worker_id)
        orch.complete(w.worker_id, output_ref="result.json",
                      evidence_refs=["ev-001", "ev-002"], reason="criterion-X done in result.json")
        rec = orch.ledger.load(w.worker_id)
        self.assertEqual(rec.results["output_ref"], "result.json")
        self.assertIn("ev-001", rec.results["evidence_refs"])
        events = orch.ledger.events.entries(w.worker_id)
        types = [e["event_type"] for e in events]
        self.assertIn("WORKER_COMPLETE", types)
        self.assertIn("WORKER_CREATED", types)


class OR14_ContextAuthorityInheritance(unittest.TestCase):
    def test_OR14_selected_context_no_leakage(self):
        mem_root = make_root()
        from paios_memory.store import MemoryStore
        from paios_memory.records import MemoryRecord
        store = MemoryStore(mem_root)
        rec = store.remember(MemoryRecord(
            content="engineering secret detail xyz", type="OBSERVATION",
            source_kind="AGENT", source_ref="test://fixture", tags=["eng"],
            sensitivity="PERSONAL"))
        pub = store.remember(MemoryRecord(
            content="public task brief alpha", type="OBSERVATION",
            source_kind="OWNER", source_ref="test://fixture", tags=["brief"],
            sensitivity="PUBLIC"))
        cb = ContextBuilder(mem_root)
        pkg = cb.build(ContextRequest(
            task=TaskSpec(task_id="TASK-c", objective="public task brief alpha"),
            inheritance_mode="SELECTED", selected_memory_ids=[pub.memory_id, rec.memory_id],
            max_sensitivity="PUBLIC", store=store))
        contents = json.dumps(pkg)
        self.assertIn("public task brief alpha", contents)
        self.assertNotIn("engineering secret detail xyz", contents)   # no leakage
        self.assertIn(rec.memory_id, pkg["inheritance"]["excluded_refs"])


import json  # noqa: E402  (used by OR14)

class OR15_Persistence(unittest.TestCase):
    def test_OR15_process_boundary(self):
        root = make_root()
        # --- "process A": create, mutate, persist ---
        orch_a = Orchestrator(root)
        t = orch_a.create_task(objective="o", scope="read-only research",
                               allowed_tools=[], authority_scope="task-scoped read-only",
                               constraints=[], acceptance_criteria=["c"],
                               expected_output="e", evidence_requirements=["r"])
        w = orch_a.spawn_worker(t.task_id)
        orch_a.start(w.worker_id)
        orch_a.complete(w.worker_id, output_ref="r.txt", evidence_refs=["ev-1"])
        w2 = orch_a.spawn_worker(t.task_id)
        orch_a.start(w2.worker_id)
        # --- "process B": fresh orchestrator reconstructs ---
        orch_b = Orchestrator(root)
        loaded = orch_b.ledger.load(w.worker_id)
        self.assertEqual(loaded.worker_id, w.worker_id)
        self.assertEqual(loaded.state, "COMPLETE")
        tasks = orch_b._load_tasks()
        self.assertIn(t.task_id, tasks)
        incomplete = [x for x in orch_b.ledger.all_workers()
                      if x.state not in ("COMPLETE", "CANCELLED")]
        self.assertEqual([x.worker_id for x in incomplete], [w2.worker_id])


class OR16_StaleWorker(unittest.TestCase):
    def test_OR16_stale_reconciliation(self):
        root = make_root()
        orch_a = Orchestrator(root)
        t = orch_a.create_task(objective="o", scope="read-only research",
                               allowed_tools=[], authority_scope="task-scoped read-only",
                               constraints=[], acceptance_criteria=["c"],
                               expected_output="e", evidence_requirements=["r"])
        w = orch_a.spawn_worker(t.task_id)
        orch_a.start(w.worker_id)          # left RUNNING across "restart"
        orch_b = Orchestrator(root)
        stale = orch_b.reconcile_after_restart()
        self.assertEqual([x.worker_id for x in stale], [w.worker_id])
        rec = orch_b.ledger.load(w.worker_id)
        self.assertTrue(rec.stale)
        self.assertTrue(rec.requires_reconciliation)
        self.assertEqual(rec.state, "RUNNING")     # NOT treated as complete
        # dispatcher surfaces reconciliation need
        d = orch_b.dispatcher.decide_worker(rec)
        self.assertEqual(d.action, "REDIRECT")


class OR17_ParentAggregation(unittest.TestCase):
    def test_OR17_mixed_outcomes(self):
        root = make_root()
        orch = Orchestrator(root)
        t = orch.create_task(objective="o", scope="read-only research",
                             allowed_tools=[], authority_scope="task-scoped read-only",
                             constraints=[], acceptance_criteria=["criterion-Z done"],
                             expected_output="e", evidence_requirements=["r"])
        kids = []
        for i in range(3):
            w = orch.spawn_worker(t.task_id)
            orch.start(w.worker_id)
            kids.append(w.worker_id)
        orch.complete(kids[0], output_ref="a.txt", evidence_refs=["ev-a"],
                      reason="criterion-Z done in a.txt")
        orch.fail(kids[1], error_type="hard", message="unrecoverable")
        orch.complete(kids[2], output_ref="c.txt", evidence_refs=["ev-c"],
                      reason="criterion-Z done in c.txt")
        res = orch.acceptor.aggregate_parent(
            t.task_id, kids,
            criterion_evidence={"criterion-Z done": "ev-a"})
        self.assertFalse(res.accepted)      # one success cannot hide one failure
        self.assertTrue(any("kids" not in r and "not COMPLETE" in r for r in res.reasons))


class OR18_RecoveryWithoutScopeExpansion(unittest.TestCase):
    def test_OR18_bounded_recovery(self):
        root = make_root()
        orch = Orchestrator(root)
        t = orch.create_task(objective="o", scope="read-only research",
                             allowed_tools=[], authority_scope="task-scoped read-only",
                             constraints=["no external communication"],
                             acceptance_criteria=["c"], expected_output="e",
                             evidence_requirements=["r"])
        w = orch.spawn_worker(t.task_id)
        orch.start(w.worker_id)
        orch.fail(w.worker_id, error_type="scope", message="needs broader access to proceed")
        sup = orch.supervisor
        out = sup.recover(w.worker_id, strategy="replace", reason="worker requested scope expansion; denied")
        new = out["worker"]
        self.assertEqual(new.scope, "read-only research")         # scope NOT widened
        self.assertEqual(new.authority_scope, "task-scoped read-only")
        self.assertEqual(new.constraints, ["no external communication"])
        old = orch.ledger.load(w.worker_id)
        self.assertEqual(old.state, "STOPPED")                    # evidence preserved
        self.assertTrue(old.errors)


class OR19_DispatcherExecutorSeparation(unittest.TestCase):
    def test_OR19_adapter_boundary(self):
        # portable decisions do not touch runtime APIs
        d = Dispatcher()
        dec = d.decide_task("T1", {})
        self.assertEqual(dec.action, "EXECUTE")
        # capability discovery distinguishes layers
        caps = ExecutorCapabilities(runtime_id="some-runtime",
                                    runtime_supported={"start_worker": True})
        self.assertEqual(caps.classify("start_worker"), "RUNTIME_SUPPORTED")
        self.assertEqual(caps.classify("model_routing"), "RUNTIME_UNSUPPORTED")
        self.assertEqual(caps.classify("nonexistent_op"), "UNSUPPORTED")
        # base adapter refuses unsupported ops
        ex = Executor()
        with self.assertRaises(NotImplementedError):
            ex.start_worker("WRK-1", None)


class OR20_Closeout(unittest.TestCase):
    def test_OR20_closeout(self):
        root = make_root()
        cp_store = CheckpointStore(Path(root) / "checkpoints", repo_path=".")
        orch = Orchestrator(root, checkpoint_store=cp_store)
        t = orch.create_task(objective="o", scope="read-only research",
                             allowed_tools=[], authority_scope="task-scoped read-only",
                             constraints=[], acceptance_criteria=["criterion-Q done"],
                             expected_output="e", evidence_requirements=["r"])
        kids = [orch.spawn_worker(t.task_id).worker_id for _ in range(2)]
        for k in kids:
            orch.start(k)
        orch.complete(kids[0], output_ref="a.txt", evidence_refs=["ev-a"],
                      reason="criterion-Q done in a.txt")
        orch.complete(kids[1], output_ref="b.txt", evidence_refs=["ev-b"],
                      reason="criterion-Q done in b.txt")
        res = orch.acceptor.aggregate_parent(t.task_id, kids,
                                             criterion_evidence={"criterion-Q done": "ev-a"})
        self.assertTrue(res.accepted)
        chk_id = orch.write_checkpoint(t.task_id, evidence_refs=["ev-a", "ev-b"])
        self.assertIsNotNone(chk_id)
        chk = cp_store.load_checkpoint(chk_id)
        self.assertEqual(len(chk.workers), 2)
        self.assertEqual(chk.blockers, [])
        self.assertEqual(chk.next_actions, [])   # nothing incomplete remains
        # canonical closeout possible without replaying worker conversations
        self.assertTrue(all(w["state"] == "COMPLETE" for w in chk.workers))


class AdversarialTests(unittest.TestCase):
    def test_scope_escalation(self):
        parent = sample_task()
        with self.assertRaises(PermissionError):
            delegate(parent, objective="x", scope="read-only research, external send",
                     allowed_tools=[], authority_scope="task-scoped read-only",
                     constraints=[], acceptance_criteria=["c"], evidence_requirements=[])

    def test_authority_escalation(self):
        parent = sample_task()
        with self.assertRaises(PermissionError) as cm:
            delegate(parent, objective="x", scope="read-only research",
                     allowed_tools=[], authority_scope="task-scoped read-only, global admin",
                     constraints=[], acceptance_criteria=["c"], evidence_requirements=[])
        self.assertEqual(str(cm.exception), AUTHORITY_ESCALATION_REJECTED)

    def test_failed_sibling_blocks_parent_success(self):
        root = make_root()
        orch = Orchestrator(root)
        t = orch.create_task(objective="o", scope="read-only research",
                             allowed_tools=[], authority_scope="task-scoped read-only",
                             constraints=[], acceptance_criteria=["criterion-W done"],
                             expected_output="e", evidence_requirements=["r"])
        good = orch.spawn_worker(t.task_id)
        bad = orch.spawn_worker(t.task_id)
        orch.start(good.worker_id); orch.start(bad.worker_id)
        orch.complete(good.worker_id, output_ref="ok.txt", evidence_refs=["ev-g"])
        orch.fail(bad.worker_id, error_type="hard", message="crashed")
        res = orch.acceptor.aggregate_parent(
            t.task_id, [good.worker_id, bad.worker_id],
            criterion_evidence={"criterion-W done": "ev-g"})
        self.assertFalse(res.accepted)

    def test_stale_worker_across_restart(self):
        root = make_root()
        orch_a = Orchestrator(root)
        t = orch_a.create_task(objective="o", scope="read-only research",
                               allowed_tools=[], authority_scope="task-scoped read-only",
                               constraints=[], acceptance_criteria=["c"],
                               expected_output="e", evidence_requirements=["r"])
        w = orch_a.spawn_worker(t.task_id)
        orch_a.start(w.worker_id)
        Orchestrator(root).reconcile_after_restart()
        rec = Orchestrator(root).ledger.load(w.worker_id)
        self.assertTrue(rec.requires_reconciliation)
        self.assertNotEqual(rec.state, "COMPLETE")

    def test_invalid_transition(self):
        root = make_root()
        ledger = WorkerLedger(root)
        w = ledger.create(task_id="TASK-inv", parent_task_id=None, role="worker",
                          runtime="t", model_provider="u", objective="o", scope="s",
                          authority_scope="a", allowed_tools=[], constraints=[],
                          acceptance_criteria=["c"], context_package=None)
        with self.assertRaises(InvalidTransition):
            ledger.transition(w.worker_id, "COMPLETE")   # PENDING -> COMPLETE

    def test_dependency_violation(self):
        g = DependencyGraph()
        g.declare("B", ["A"])
        self.assertEqual(g.readiness("B", {"A": "PENDING"}), "BLOCKED")
        self.assertEqual(g.readiness("B", {"A": "RUNNING"}), "BLOCKED")

    def test_context_leakage(self):
        mem_root = make_root()
        from paios_memory.store import MemoryStore
        from paios_memory.records import MemoryRecord
        store = MemoryStore(mem_root)
        secret = store.remember(MemoryRecord(
            content="confidential salary data", type="OBSERVATION",
            source_kind="OWNER", source_ref="test://fixture", tags=["salary"],
            sensitivity="PERSONAL"))
        cb = ContextBuilder(mem_root)
        pkg = cb.build(ContextRequest(
            task=TaskSpec(task_id="TASK-l", objective="build report"),
            inheritance_mode="SELECTED", selected_memory_ids=[secret.memory_id],
            max_sensitivity="INTERNAL", store=store))
        self.assertNotIn("confidential salary data", json.dumps(pkg))

    def test_evidence_loss_prevented(self):
        root = make_root()
        orch = Orchestrator(root)
        t = orch.create_task(objective="o", scope="read-only research",
                             allowed_tools=[], authority_scope="task-scoped read-only",
                             constraints=[], acceptance_criteria=["c"],
                             expected_output="e", evidence_requirements=["r"])
        w = orch.spawn_worker(t.task_id)
        orch.start(w.worker_id)
        orch.fail(w.worker_id, error_type="err", message="first failure evidence")
        sup = orch.supervisor
        new = sup.recover(w.worker_id, strategy="replace", reason="replace worker")["worker"]
        old = orch.ledger.load(w.worker_id)
        self.assertEqual(old.errors[0]["message"], "first failure evidence")
        self.assertIn("replaced by", old.progress["summary"])
        self.assertNotEqual(new.worker_id, w.worker_id)


if __name__ == "__main__":
    unittest.main()
