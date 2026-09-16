"""OR-15 persistence proof across REAL OS process boundaries.

Process A (subprocess): creates a task, spawns workers, starts them, completes
one, leaves one RUNNING (stale candidate), persists, exits.
Process B (subprocess): boots a fresh orchestrator, reloads the ledger purely
from disk, reconstructs hierarchy, reconciles stale RUNNING work, and prints a
JSON report on stdout. The parent test asserts the report's contents.

Engine behavior is unchanged; this test only exercises the existing durable
storage path from two genuinely separate Python processes.

Run: python -m unittest tests.test_phase9_subprocess -v
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ENGINE_ROOT = Path(__file__).resolve().parents[1]
MEMORY_ROOT = ENGINE_ROOT.parent / "memory_engine"

# Child-process scripts. They are plain Python sources executed with
# `sys.executable` so both sides are genuinely separate OS processes.

PROCESS_A = r'''
import json, sys
sys.path.insert(0, {engine_root!r}); sys.path.insert(0, {memory_root!r})
from paios_orch import Orchestrator

root = {state_root!r}
orch = Orchestrator(root)
t = orch.create_task(
    objective="cross-process persistence proof", scope="read-only research",
    allowed_tools=[], authority_scope="task-scoped read-only",
    constraints=["no external communication"],
    acceptance_criteria=["criterion-P done"], expected_output="report",
    evidence_requirements=["ref"])
parent_w = orch.spawn_worker(t.task_id, role="coordinator")
good = orch.spawn_worker(t.task_id, parent_worker_id=parent_w.worker_id)
stale = orch.spawn_worker(t.task_id, parent_worker_id=parent_w.worker_id)
orch.start(good.worker_id)
orch.start(stale.worker_id)                 # left RUNNING across the boundary
orch.complete(good.worker_id, output_ref="good.txt", evidence_refs=["ev-good"],
              reason="criterion-P done in good.txt")
print(json.dumps({{"task_id": t.task_id, "parent": parent_w.worker_id,
                   "good": good.worker_id, "stale": stale.worker_id}}))
'''

PROCESS_B = r'''
import json, sys
sys.path.insert(0, {engine_root!r}); sys.path.insert(0, {memory_root!r})
from paios_orch import Orchestrator

root = {state_root!r}
ids = json.loads({ids_json!r})
orch = Orchestrator(root)                   # fresh boot; nothing in memory

# ledger reloaded from disk
w_good = orch.ledger.load(ids["good"])
w_stale = orch.ledger.load(ids["stale"])
# hierarchy reconstructed from disk records
chain = orch.ledger.ancestry(ids["stale"])
# incomplete work identified
incomplete = [w.worker_id for w in orch.ledger.all_workers()
              if w.state not in ("COMPLETE", "CANCELLED")]
# stale reconciliation
reconciled = orch.reconcile_after_restart()
stale_after = orch.ledger.load(ids["stale"])

print(json.dumps({{
    "task_registered": ids["task_id"] in orch._load_tasks(),
    "good_state": w_good.state,
    "good_evidence": w_good.results["evidence_refs"],
    "stale_state_on_reload": w_stale.state,
    "ancestry_chain": [w.worker_id for w in chain],
    "incomplete_from_disk": sorted(incomplete),
    "reconciled_ids": sorted(w.worker_id for w in reconciled),
    "stale_flag": stale_after.stale,
    "needs_reconciliation": stale_after.requires_reconciliation,
    "stale_state_after": stale_after.state,
}}))
'''


class OR15SubprocessPersistence(unittest.TestCase):
    def test_OR15_real_process_boundary(self):
        state_root = tempfile.mkdtemp(prefix="paios_orch_xproc_")
        fmt = {"engine_root": str(ENGINE_ROOT), "memory_root": str(MEMORY_ROOT),
               "state_root": state_root}

        # --- Process A: create, mutate, persist, exit ------------------------
        code_a = PROCESS_A.format(**fmt)
        proc_a = subprocess.run([sys.executable, "-c", code_a],
                                capture_output=True, text=True, timeout=120,
                                cwd=str(ENGINE_ROOT))
        self.assertEqual(proc_a.returncode, 0,
                         f"Process A failed:\n{proc_a.stderr}")
        ids = json.loads(proc_a.stdout.strip().splitlines()[-1])
        self.assertNotEqual(ids["good"], ids["stale"])

        # --- Process B: fresh boot from disk only ----------------------------
        code_b = PROCESS_B.format(**fmt, ids_json=json.dumps(ids))
        proc_b = subprocess.run([sys.executable, "-c", code_b],
                                capture_output=True, text=True, timeout=120,
                                cwd=str(ENGINE_ROOT))
        self.assertEqual(proc_b.returncode, 0,
                         f"Process B failed:\n{proc_b.stderr}")
        report = json.loads(proc_b.stdout.strip().splitlines()[-1])

        # --- assertions on Process B's independently derived report ----------
        self.assertTrue(report["task_registered"])
        self.assertEqual(report["good_state"], "COMPLETE")
        self.assertEqual(report["good_evidence"], ["ev-good"])
        self.assertEqual(report["stale_state_on_reload"], "RUNNING")
        # hierarchy: stale -> coordinator parent, from disk only
        self.assertEqual(report["ancestry_chain"], [ids["stale"], ids["parent"]])
        # incomplete work identified from disk
        self.assertIn(ids["stale"], report["incomplete_from_disk"])
        self.assertNotIn(ids["good"], report["incomplete_from_disk"])
        # stale reconciliation: flagged, not completed, evidence preserved
        self.assertEqual(report["reconciled_ids"], [ids["stale"]])
        self.assertTrue(report["stale_flag"])
        self.assertTrue(report["needs_reconciliation"])
        self.assertEqual(report["stale_state_after"], "RUNNING")


if __name__ == "__main__":
    unittest.main()
