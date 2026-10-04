"""Phase 14 second-runtime real execution tests: hermes-agent via Hermes CLI.

Mirrors the RT-01..RT-14 real-execution pattern of test_phase14.py for the
SECOND verified runtime. Real executions here are bounded and read-only:
prompt-echo probes, a real repository-file task, reproducibility, and
provider-failure normalization. Sandbox/write isolation is NOT claimed for
hermes (--safe-mode observed read-capable but not write-isolating), so no
write-refusal test exists — the limitation is asserted instead.

Requires: hermes CLI on PATH + Nous Portal auth + free model
poolside/laguna-xs-2.1:free (verified live 2026-10-03).
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from paios_runtime import (
    CapabilityRegistry, ExecutionRequest, ExecutionStatus, Lifecycle,
    ParityEnforcer, RuntimeCapabilityRecord, HermesRuntimeAdapter,
    VerificationState,
)


def make_request(**over):
    fields = dict(
        task_id="TASK-hr", objective="bounded repository-local inspection",
        authority_context="policy-phase14",
        acceptance_criteria=["summary names the requested file"],
        idempotency_token="hr-token", evidence_requirements=["output_ref"],
        inputs={"prompt": "Reply with exactly: HERMES-PROBE-OK"},
    )
    fields.update(over)
    return ExecutionRequest(**fields)


def real_adapter(**over):
    return HermesRuntimeAdapter(**over)


@unittest.skipUnless(HermesRuntimeAdapter().health() == "AVAILABLE",
                     "hermes CLI not available")
class HermesRealExecutionTests(unittest.TestCase):
    """Tests that invoke the REAL hermes runtime (bounded, read-only)."""

    @classmethod
    def setUpClass(cls):
        cls.adapter = real_adapter()
        cls.binary = cls.adapter.binary_path()
        cls.auth = cls.adapter.auth_state()

    def test_HR01_adapter_discovery(self):
        self.assertIsNotNone(self.binary)
        self.assertIn("hermes", Path(self.binary).name.lower())
        self.assertEqual(self.adapter.runtime_id, "hermes-agent")

    def test_HR02_health_and_auth(self):
        self.assertEqual(self.adapter.health(), "AVAILABLE")
        self.assertEqual(self.auth, "AUTHENTICATED")   # Nous Portal logged in

    def test_HR03_capability_lifecycle_promotion(self):
        root = tempfile.mkdtemp()
        reg = CapabilityRegistry(root)
        rec = RuntimeCapabilityRecord(
            runtime_id=self.adapter.runtime_id,
            capabilities=set(self.adapter.provided_capabilities),
            lifecycle=Lifecycle.INSTALLED,
            verification=VerificationState.CLAIMED,
            model_access="SINGLE", tool_access="SINGLE", execution_mode="SYNC",
            structured_output=False, streaming=False, parallelism=False,
            long_running=False, web_capability="UNKNOWN",
            auth_state="AUTHENTICATED",
            limitations=["no write isolation under --safe-mode (observed)",
                         "no structured/usage output",
                         "no cancellation"],
            evidence_refs=["local-cli://hermes --version -> v0.21.3"])
        reg.register(rec)
        self.assertFalse(Lifecycle.satisfies(rec.lifecycle, Lifecycle.VERIFIED))
        rec.mark_verified(
            evidence_ref="hermes://live-exec/nous/poolside-laguna-xs-2.1-free/2026-10-03",
            timestamp="2026-10-03T00:00:00Z")
        self.assertTrue(Lifecycle.satisfies(rec.lifecycle, Lifecycle.VERIFIED))
        reg.register(rec)
        reg2 = CapabilityRegistry(root)
        self.assertEqual(reg2.get("hermes-agent").verification, "VERIFIED")

    def test_HR04_HR05_real_request_result(self):
        req = make_request(task_id="TASK-hr04")
        res = self.adapter.execute(req)
        self.assertEqual(res.status, ExecutionStatus.COMPLETED)
        self.assertEqual(res.runtime_id, "hermes-agent")
        self.assertEqual(res.request_fingerprint, req.fingerprint())
        self.assertTrue(res.output_ref and "HERMES-PROBE-OK" in res.output_ref)
        self.assertTrue(res.evidence_refs)
        self.assertEqual(res.verification.get("provider"), "nous")

    def test_HR06_result_verification(self):
        res = self.adapter.execute(make_request(task_id="TASK-hr06"))
        verdict = self.adapter.verify(res)
        self.assertTrue(verdict["verified"])

    def test_HR07_identity_preservation(self):
        res = self.adapter.execute(make_request(task_id="TASK-hr07"))
        self.assertEqual(res.adapter_id, "hermes-cli-adapter")
        self.assertEqual(res.request_fingerprint,
                         make_request(task_id="TASK-hr07").fingerprint())

    def test_HR08_real_repo_task_reproducible(self):
        # real repository-local task, run twice for reproducibility
        ws = Path(__file__).resolve().parents[1] / "paios_runtime"
        a = real_adapter(workspace_root=str(ws))
        prompt = ("Read execution.py in the current directory and reply with "
                  "ONLY the 6 ExecutionStatus values, one per line.")
        outputs = []
        for i, tid in enumerate(("TASK-hr08a", "TASK-hr08b")):
            req = make_request(task_id=tid, objective="read ExecutionStatus values",
                               acceptance_criteria=["all six status values returned"],
                               inputs={"prompt": prompt})
            res = a.execute(req)
            self.assertEqual(res.status, ExecutionStatus.COMPLETED, res.error)
            outputs.append(res.output_ref)
        for value in ("PENDING", "RUNNING", "COMPLETED", "FAILED", "UNKNOWN", "TIMEOUT"):
            self.assertIn(value, outputs[0])
            self.assertIn(value, outputs[1])

    def test_HR09_parity_enforcement_real(self):
        ws = Path(tempfile.mkdtemp())
        marker = "PAIOS-HR09-MARKER-LINE"
        (ws / "subject_file.txt").write_text(marker + "\nsecond line\n",
                                             encoding="utf-8")
        a = real_adapter(workspace_root=str(ws))
        req = make_request(
            task_id="TASK-hr09",
            objective="read subject_file.txt and return its first line exactly",
            acceptance_criteria=["first line returned exactly"],
            inputs={"prompt": "This directory contains subject_file.txt. Reply "
                              "with ONLY its first line, character for character."})
        res = a.execute(req)
        self.assertEqual(res.status, ExecutionStatus.COMPLETED, res.error)
        self.assertIn(marker, res.output_ref)
        check = ParityEnforcer().check(req, res)
        self.assertTrue(check.consistent, check.violations)

    def test_HR12_authority_propagation_real(self):
        a = real_adapter(workspace_root=tempfile.mkdtemp())
        req = make_request(task_id="TASK-hr12",
                           inputs={"prompt": "Reply with exactly: AUTH-ECHO-HR"})
        res = a.execute(req)
        self.assertEqual(res.status, ExecutionStatus.COMPLETED)
        self.assertEqual(res.request_fingerprint, req.fingerprint())

    def test_HR14_idempotency_real(self):
        r1 = self.adapter.execute(make_request(task_id="TASK-hr14"))
        r2 = self.adapter.execute(make_request(task_id="TASK-hr14"))
        self.assertEqual(r1.request_fingerprint, r2.request_fingerprint)
        self.assertNotEqual(r1.execution_id, r2.execution_id)

    def test_HR15_provider_failure_normalization(self):
        # nonexistent model -> provider error transcript -> FAILED (never COMPLETED)
        bad = real_adapter(model="nonexistent-model-xyz")
        res = bad.execute(make_request(task_id="TASK-hr15"))
        self.assertEqual(res.status, ExecutionStatus.FAILED)
        self.assertTrue(res.error)   # surfaced, not swallowed

    def test_HR16_timeout_handling(self):
        short = real_adapter(timeout_seconds=1)
        res = short.execute(make_request(task_id="TASK-hr16"))
        self.assertEqual(res.status, ExecutionStatus.TIMEOUT)
        self.assertEqual(res.error_type, "deadline_exceeded")
        self.assertIsNone(res.output_ref)

    def test_HR17_no_write_isolation_claimed(self):
        # honest limitation: --safe-mode does NOT provide write isolation
        self.assertNotIn("read_only_sandbox", self.adapter.provided_capabilities)
        self.assertNotIn("structured_output", self.adapter.provided_capabilities)


if __name__ == "__main__":
    unittest.main()
