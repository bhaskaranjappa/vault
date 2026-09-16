"""Executable Phase 8 tests: MC-01..MC-09 and CT-01..CT-08.

All state lives in temporary directories; canonical memory is never touched.
Run:  python -m unittest tests.test_phase8 -v   (from 13_AUTOMATION/memory_engine)
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from paios_memory import (
    Checkpoint, CheckpointStore, ContextBuilder, ContextRequest, MemoryRecord,
    MemoryStore, RetrievalQuery, Retriever, TaskSpec, resume,
)


def mk(content, **kw):
    kw.setdefault("source_kind", "OWNER")
    kw.setdefault("source_ref", "test://fixture")
    kw.setdefault("captured_at", "2026-09-15T00:00:00Z")
    return MemoryRecord(content=content, **kw)


class Phase8Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="paios-phase8-"))
        self.state = self.tmp / "state"
        self.store = MemoryStore(self.state)
        self.retriever = Retriever(self.store)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


class MemoryTests(Phase8Base):
    def test_MC01_explicit_memory_write(self):
        rec = self.store.remember(mk("User prefers dark mode for all UI work.",
                                     type="PREFERENCE", tags=["ui"]))
        got = self.store.get(rec.memory_id)
        self.assertIsNotNone(got)
        self.assertEqual(got.content, "User prefers dark mode for all UI work.")
        self.assertEqual(got.source_kind, "OWNER")
        with self.assertRaises(ValueError):
            self.store.remember(mk("   "))
        with self.assertRaises(ValueError):  # secrets rejected
            self.store.remember(mk("the api_key = sk-abcdef1234567890"))

    def test_MC02_persistence_across_sessions(self):
        rec = self.store.remember(mk("PAIOS memory engine uses file-backed storage.",
                                     type="FACT", project="personal-ai-os"))
        # Session boundary: drop all in-memory references, build a fresh store.
        del rec
        fresh_store = MemoryStore(self.state)
        got = fresh_store.get([r.memory_id for r in fresh_store.all_records()][0])
        self.assertIsNotNone(got)
        self.assertIn("file-backed", got.content)

    def test_MC03_relevance_gating(self):
        self.store.remember(mk("User's favourite coffee order is a flat white.",
                               tags=["personal"], sensitivity="PERSONAL",
                               source_kind="CONVERSATION"))
        self.store.remember(mk("PAIOS memory engine implements lexical retrieval.",
                               type="FACT", project="personal-ai-os",
                               tags=["memory", "retrieval"]))
        results = self.retriever.retrieve(RetrievalQuery(
            text="PAIOS memory engine lexical retrieval implementation",
            project="personal-ai-os"))
        ids = [s.record.memory_id for s in results]
        self.assertTrue(any("lexical retrieval" in s.record.content for s in results))
        self.assertTrue(all("coffee" not in s.record.content for s in results),
                        "irrelevant personal memory entered engineering context")

    def test_MC04_sensitivity_gating(self):
        pub = self.store.remember(mk("Project uses Python 3.14.", sensitivity="PUBLIC"))
        personal = self.store.remember(mk("User's home address is private data.",
                                         sensitivity="PERSONAL"))
        results = self.retriever.retrieve(RetrievalQuery(
            text="private data home address python project",
            max_sensitivity="INTERNAL"))
        ids = [s.record.memory_id for s in results]
        self.assertNotIn(personal.memory_id, ids)
        self.assertIn(pub.memory_id, ids)

    def test_MC05_provenance_preservation(self):
        rec = self.store.remember(mk("Decision: use JSON for record storage.",
                                     type="DECISION", source_kind="OWNER",
                                     source_ref="task://phase8/decision-log"))
        got = self.store.get(rec.memory_id)
        self.assertEqual(got.source_kind, "OWNER")
        self.assertEqual(got.source_ref, "task://phase8/decision-log")
        self.assertTrue(got.created_at and got.updated_at)

    def test_MC06_stated_vs_inferred(self):
        stated = self.store.remember(mk("User stated the deadline is Friday.",
                                        classification="STATED"))
        inferred = self.store.remember(mk("Deadline may slip based on velocity.",
                                          classification="INFERRED",
                                          confidence="LOW",
                                          source_kind="AGENT"))
        self.assertEqual(self.store.get(stated.memory_id).classification, "STATED")
        self.assertEqual(self.store.get(inferred.memory_id).classification, "INFERRED")
        # low-confidence inferred record is deprioritized, never promoted
        self.assertGreater(
            self.retriever.retrieve(RetrievalQuery(text="stated deadline Friday"))[0].score,
            min(s.score for s in self.retriever.retrieve(
                RetrievalQuery(text="stated deadline Friday"))))

    def test_MC07_conflict_preservation(self):
        old = self.store.remember(mk("Deploy target is AWS us-east-1."))
        _, new = self.store.update(old.memory_id, "Deploy target is AWS eu-west-1.",
                                   source_kind="OWNER", source_ref="test://update",
                                   conflict=True)
        preserved = self.store.get(old.memory_id)
        self.assertEqual(preserved.status, "CONFLICTING")
        self.assertEqual(preserved.content, "Deploy target is AWS us-east-1.")
        self.assertIn(old.memory_id, new.conflict_refs)
        self.assertEqual(len(self.store.list_conflicts()), 1)
        # both remain individually discoverable
        self.assertIsNotNone(self.store.get(new.memory_id))

    def test_MC08_current_state_precedence(self):
        old = self.store.remember(mk("The build tool is Maven.",
                                     source_kind="OWNER",
                                     captured_at="2026-01-01T00:00:00Z"))
        _, new = self.store.update(old.memory_id, "The build tool is Gradle.",
                                   source_kind="CANONICAL_FILE",
                                   source_ref="canonical://build.md",
                                   captured="now")
        # stale record must not outrank the newer authoritative one
        results = self.retriever.retrieve(RetrievalQuery(text="build tool"))
        self.assertEqual(results[0].record.content, "The build tool is Gradle.")
        self.assertEqual(self.store.get(old.memory_id).status, "SUPERSEDED")
        self.assertEqual(self.store.get(old.memory_id).content, "The build tool is Maven.")

    def test_MC09_invalidation(self):
        rec = self.store.remember(mk("Temporary assumption: API v2 deprecated."))
        self.store.invalidate(rec.memory_id, reason="contradicted")
        results = self.retriever.retrieve(RetrievalQuery(text="API v2 deprecated"))
        self.assertEqual([s.record.memory_id for s in results], [])
        got = self.store.get(rec.memory_id)  # auditable transition, still on disk
        self.assertEqual(got.status, "INVALIDATED")


class ContextTests(Phase8Base):
    def _fixture(self):
        m1 = self.store.remember(mk("Phase 8 requires lexical retrieval first.",
                                    project="personal-ai-os", tags=["phase8"]))
        self.store.remember(mk("User's phone number is personal data.",
                               sensitivity="PERSONAL", tags=["personal"]))
        return m1

    def _req(self, **kw):
        task = TaskSpec(task_id="TASK-phase8-test",
                        objective="Implement PAIOS phase 8 memory engine",
                        scope="13_AUTOMATION/memory_engine",
                        acceptance_criteria=["tests pass", "persistence proven"])
        defaults = dict(
            task=task,
            canonical_rules=["03_PROTOCOLS/AIOS_MEMORY_CONTEXT_PROTOCOL.md"],
            canonical_files=["03_PROTOCOLS/AIOS_MEMORY_ARCHITECTURE_V1.md"],
            adapter="06_PLATFORM_ADAPTERS/ZCODE.md",
            executor="ZCode",
            max_sensitivity="INTERNAL",
            retriever=self.retriever,
        )
        defaults.update(kw)
        return ContextRequest(**defaults)

    def test_CT01_context_package_construction(self):
        m1 = self._fixture()
        pkg = ContextBuilder(self.state).build(self._req(
            selected_memory_ids=[m1.memory_id], inheritance_mode="SELECTED"))
        for key in ("context_package_id", "task_id", "created_at", "source_checkpoint",
                    "mission", "policy", "knowledge", "runtime", "state", "evidence",
                    "inheritance", "budget", "sensitivity"):
            self.assertIn(key, pkg)
        self.assertEqual(pkg["inheritance"]["mode"], "SELECTED")

    def test_CT02_minimal_context(self):
        pkg = ContextBuilder(self.state).build(self._req(inheritance_mode="NONE"))
        self.assertEqual(pkg["knowledge"]["selected_records"], [])
        self.assertTrue(pkg["policy"]["canonical_rules"])  # policy still present
        self.assertTrue(pkg["mission"]["objective"])

    def test_CT03_selective_inheritance(self):
        m1 = self._fixture()
        pkg = ContextBuilder(self.state).build(self._req(
            selected_memory_ids=[m1.memory_id], inheritance_mode="SELECTED"))
        ids = [r["memory_id"] for r in pkg["knowledge"]["selected_records"]]
        self.assertEqual(ids, [m1.memory_id])  # only what was selected

    def test_CT04_context_budgeting(self):
        m1 = self._fixture()
        filler = [self.store.remember(mk(f"Filler memory {i} about deployment lore." * 20,
                                         project="personal-ai-os"))
                  for i in range(5)]
        b = ContextBuilder(self.state)
        pkg_items = b.build(self._req(
            selected_memory_ids=[m1.memory_id] + [f.memory_id for f in filler],
            inheritance_mode="SELECTED", max_items=2))
        self.assertLessEqual(len(pkg_items["knowledge"]["selected_records"]), 2)
        pkg_chars = b.build(self._req(
            selected_memory_ids=[m1.memory_id] + [f.memory_id for f in filler],
            inheritance_mode="SELECTED", max_chars=400))
        self.assertLessEqual(
            len(json.dumps(pkg_chars["knowledge"]["selected_records"])), 400 - 250)
        # protected material survives truncation
        self.assertTrue(pkg_chars["mission"]["acceptance_criteria"])
        self.assertTrue(pkg_chars["policy"]["canonical_rules"])

    def test_CT05_checkpoint_creation(self):
        chk = CheckpointStore(self.state / "checkpoints").create_checkpoint(
            Checkpoint(task_id="TASK-phase8-test",
                       objective="Implement phase 8",
                       acceptance_criteria=["tests pass"],
                       completed=[{"action": "write engine", "status": "COMPLETE",
                                   "evidence": ["commit:abc"]}],
                       next_actions=["run test suite"]))
        got = CheckpointStore(self.state / "checkpoints").load_checkpoint(chk.checkpoint_id)
        self.assertEqual(got.objective, "Implement phase 8")
        self.assertEqual(got.completed[0]["action"], "write engine")
        self.assertIn(got.repository["working_tree"], ("CLEAN", "DIRTY", "UNKNOWN"))

    def test_CT06_checkpoint_reconstruction(self):
        store = CheckpointStore(self.state / "checkpoints")
        chk = store.create_checkpoint(Checkpoint(
            task_id="TASK-phase8-test", objective="Implement phase 8",
            next_actions=["run tests"], context_package=None))
        # new process/store instance reconstructs task state from disk only
        fresh = CheckpointStore(self.state / "checkpoints")
        got = fresh.load_checkpoint(chk.checkpoint_id)
        self.assertEqual(got.next_actions, ["run tests"])
        self.assertEqual(got.task_id, chk.task_id)

    def test_CT07_state_verification_on_resume(self):
        store = CheckpointStore(self.state / "checkpoints", repo_path=self.tmp)
        chk = store.create_checkpoint(Checkpoint(
            task_id="TASK-phase8-test", objective="Implement phase 8",
            repository={"ref": "git", "branch": "main",
                        "head": "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
                        "working_tree": "CLEAN"},
            next_actions=["continue"]))
        report = resume(store, chk.checkpoint_id)
        self.assertFalse(report["safe_to_continue"])
        self.assertTrue(report["discrepancies"])  # HEAD mismatch detected
        self.assertEqual(report["next_action"], "continue")

    def test_CT08_compaction_readiness(self):
        m1 = self._fixture()
        store = CheckpointStore(self.state / "checkpoints")
        chk = store.create_checkpoint(Checkpoint(
            task_id="TASK-phase8-test", objective="Implement phase 8",
            completed=[{"action": "engine core", "status": "COMPLETE",
                        "evidence": ["tests"]}],
            current_state={"phase": "testing", "active_action": None,
                           "observations": []},
            next_actions=["run suite"], evidence_refs=["tests/test_phase8.py"]))
        builder = ContextBuilder(self.state)
        pkg = builder.build(self._req(
            selected_memory_ids=[m1.memory_id],
            source_checkpoint=chk.checkpoint_id, inheritance_mode="SELECTED"))
        # checkpoint + package are sufficient to resume without conversation
        self.assertEqual(pkg["source_checkpoint"], chk.checkpoint_id)
        loaded = store.load_checkpoint(chk.checkpoint_id)
        self.assertTrue(loaded.next_actions and loaded.completed)
        stored_pkg = json.loads((self.state / "context_packages" /
                                 f"{pkg['context_package_id']}.json").read_text(encoding="utf-8"))
        self.assertEqual(stored_pkg["mission"]["objective"],
                         pkg["mission"]["objective"])
        self.assertEqual(stored_pkg["knowledge"]["selected_records"][0]["memory_id"],
                         m1.memory_id)


if __name__ == "__main__":
    unittest.main(verbosity=2)
