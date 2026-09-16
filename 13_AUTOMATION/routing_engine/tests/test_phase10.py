"""PAIOS V1+ Phase 10 tests — MR-01..MR-20 + adversarial battery.

All state is temporary; no canonical registry content is modified.
Run: python -m unittest tests.test_phase10 -v
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from paios_routing import (  # noqa: E402
    TaskCapabilityProfile, ModelCandidate, ToolCandidate, route_reasoning,
    filter_models, rank_models, filter_tools, rank_tools, route_models,
    route_tools, ModelRoute, ToolRoute, FallbackChain, FallbackTriggered,
    RouteVerifier, RoutingDecision, DecisionStore, LIFECYCLE_RANK,
    FALLBACK_REASONS,
)


def model(mid, *, caps=("coding",), lifecycle="VERIFIED", evidence=("ev-1",),
          available=True, local=False, ctx=None, reasoning=("LOW", "MEDIUM", "HIGH", "MAXIMUM"),
          cost=None, latency=None, provider="p"):
    return ModelCandidate(
        model_id=mid, provider=provider, capabilities=set(caps),
        lifecycle=lifecycle, evidence_refs=list(evidence),
        runtime_available=available, local=local, context_window=ctx,
        reasoning_levels=tuple(reasoning), cost_usd_per_1k=cost, latency_ms=latency)


def profile(**kw):
    return TaskCapabilityProfile(**kw)


class MR01_ProfileConstruction(unittest.TestCase):
    def test_MR01_capability_profile(self):
        p = profile(task_id="TASK-a", reasoning_level="HIGH", vision_required=True,
                    context_size=100000, privacy_requirement="INTERNAL_ONLY",
                    tool_requirements=["git"], output_format="markdown")
        self.assertEqual(p.required_model_capabilities(), {"vision"})
        p.validate()
        with self.assertRaises(ValueError):
            profile(reasoning_level="ABSURD").validate()
        # absent fields impose no rule
        self.assertEqual(profile().required_model_capabilities(), set())


class MR02_CapabilityFiltering(unittest.TestCase):
    def test_MR02_filter(self):
        p = profile(vision_required=True, coding_required=True)
        cands = [model("m-vis-cod", caps=("vision", "coding")),
                 model("m-cod", caps=("coding",))]
        eligible, rejected = filter_models(p, cands)
        self.assertEqual([m.model_id for m in eligible], ["m-vis-cod"])
        self.assertTrue(any("capability_mismatch" in r for r in rejected))


class MR03_ModelSelection(unittest.TestCase):
    def test_MR03_task_specific_selection(self):
        strong = model("m-strong", lifecycle="VERIFIED", evidence=("e1", "e2", "e3"))
        weak = model("m-weak", lifecycle="CONFIGURED", evidence=())
        r = route_models(profile(), [weak, strong])
        self.assertEqual(r.selected.model_id, "m-strong")   # highest evidence within constraints
        self.assertEqual([m.model_id for m in r.alternatives], ["m-weak"])
        # task-specific: different task -> possibly different winner
        p2 = profile(reliability_requirement="VERIFIED")
        r2 = route_models(p2, [weak, strong])
        self.assertEqual(r2.selected.model_id, "m-strong")
        p3 = profile(reliability_requirement="CONFIGURED")
        r3 = route_models(p3, [weak, strong])
        # evidence count dominates lifecycle, so the stronger-evidence model wins
        self.assertEqual(r3.selected.model_id, "m-strong")
        self.assertEqual([m.model_id for m in r3.alternatives], ["m-weak"])


class MR04_ReasoningRouting(unittest.TestCase):
    def test_MR04_reasoning_levels(self):
        self.assertEqual(route_reasoning("ROUTINE_TRANSFORMATION"), "LOW")
        self.assertEqual(route_reasoning("ORDINARY_ENGINEERING"), "MEDIUM")
        self.assertEqual(route_reasoning("COMPLEX_DIAGNOSIS"), "HIGH")
        self.assertEqual(route_reasoning("NOVEL_HARD_PROBLEM"), "MAXIMUM")
        # uncertainty escalates one step, never forced universally
        self.assertEqual(route_reasoning("ROUTINE_TRANSFORMATION", uncertainty="HIGH"), "MEDIUM")
        self.assertEqual(route_reasoning("ORDINARY_RESEARCH", uncertainty="HIGH"), "HIGH")
        # model without MAXIMUM support is excluded from a MAXIMUM task
        r = route_models(profile(reasoning_level="MAXIMUM"),
                         [model("m-med", reasoning=("LOW", "MEDIUM")),
                          model("m-max", reasoning=("LOW", "MEDIUM", "HIGH", "MAXIMUM"))])
        self.assertEqual(r.selected.model_id, "m-max")
        self.assertTrue(any("reasoning_level_unsupported" in x for x in r.rejected))


class MR05_Fallback(unittest.TestCase):
    def test_MR05_fallback_chain(self):
        p = profile(coding_required=True)
        r = route_models(p, [model("m-primary"), model("m-secondary")])
        chain = FallbackChain(p, r)
        nxt = chain.report_failure("TIMEOUT")
        self.assertEqual(nxt.model_id, "m-secondary")
        self.assertEqual(chain.history()[0]["reason"], "TIMEOUT")
        # terminal failure raises
        with self.assertRaises(FallbackTriggered):
            chain.report_failure("PROVIDER_FAILURE")
        # silent/unsupported reasons are refused
        with self.assertRaises(ValueError):
            FallbackChain(p, r).report_failure("FELT_LIKE_IT")


class MR06_ToolSelection(unittest.TestCase):
    def test_MR06_tool_candidates(self):
        p = profile(tool_requirements=["filesystem"])
        fs = ToolCandidate(tool_id="fs-local", type="internal",
                           capabilities={"filesystem"}, network_required=False,
                           verification_state="VERIFIED", evidence_refs=["ev"])
        web = ToolCandidate(tool_id="web-search", type="web",
                            capabilities={"search"}, verification_state="VERIFIED",
                            evidence_refs=["ev"])
        r = route_tools(p, [web, fs])
        self.assertEqual(r.selected, ["fs-local"])   # capability match beats availability
        self.assertTrue(any("capability_mismatch" in x for x in r.rejected))


class MR07_ToolLifecycle(unittest.TestCase):
    def test_MR07_lifecycle_filtering(self):
        p = profile(tool_requirements=["git"])
        unverified = ToolCandidate(tool_id="gh-unverified", type="connector",
                                   capabilities={"git"}, verification_state="CONFIGURED",
                                   evidence_refs=[])
        verified = ToolCandidate(tool_id="gh-verified", type="connector",
                                 capabilities={"git"}, verification_state="VERIFIED",
                                 evidence_refs=["ev"])
        r = route_tools(p, [unverified, verified])
        # CONFIGURED-but-uncallable ranks below VERIFIED
        self.assertEqual(r.selected, ["gh-verified", "gh-unverified"])


class MR08_InternalDataFirst(unittest.TestCase):
    def test_MR08_internal_first(self):
        p = profile(internal_data_sufficient=True, tool_requirements=["query"])
        web = ToolCandidate(tool_id="web-x", type="web", capabilities={"query"},
                            verification_state="VERIFIED", evidence_refs=["e"])
        internal = ToolCandidate(tool_id="canonical-store", type="internal",
                                 capabilities={"query"}, network_required=False,
                                 verification_state="VERIFIED", evidence_refs=["e"])
        r = route_tools(p, [web, internal])
        self.assertEqual(r.selected[0], "canonical-store")
        self.assertIn("internal-data-first", r.decision_reason)


class MR09_CurrentDataRouting(unittest.TestCase):
    def test_MR09_current_data(self):
        p = profile(current_data_required=True, tool_requirements=["search"])
        stale_mem = ToolCandidate(tool_id="memory-store", type="internal",
                                  capabilities={"search"}, network_required=False,
                                  verification_state="VERIFIED", evidence_refs=["e"])
        web = ToolCandidate(tool_id="web-current", type="web", capabilities={"search"},
                            verification_state="VERIFIED", evidence_refs=["e"])
        r = route_tools(p, [stale_mem, web])
        self.assertEqual(r.selected[0], "web-current")
        self.assertTrue(any("stale_source" in x for x in r.rejected))


class MR10_PrivacyRouting(unittest.TestCase):
    def test_MR10_privacy(self):
        p = profile(privacy_requirement="CONFIDENTIAL_LOCAL_ONLY", coding_required=True)
        external = model("cloud-x", provider="cloud")
        local = model("local-y", provider="local", local=True)
        r = route_models(p, [external, local])
        self.assertEqual(r.selected.model_id, "local-y")
        self.assertTrue(any("privacy_conflict" in x for x in r.rejected))


class MR11_AuthorityRouting(unittest.TestCase):
    def test_MR11_authority(self):
        p = profile(tool_requirements=["shell"])
        shell = ToolCandidate(tool_id="shell", type="desktop", capabilities={"shell"},
                              verification_state="VERIFIED", evidence_refs=["e"])
        r = route_tools(p, [shell], authority_allowed_tools=["fs-local"])
        self.assertEqual(r.selected, [])
        self.assertTrue(any("authority_not_permitted" in x for x in r.rejected))


class MR12_Provenance(unittest.TestCase):
    def test_MR12_decision_record(self):
        p = profile(task_id="TASK-p", worker_id="WRK-p", coding_required=True)
        r = route_models(p, [model("m-a", evidence=("e1", "e2")), model("m-b")])
        store = DecisionStore(tempfile.mkdtemp())
        dec = RoutingDecision(
            task_id=p.task_id, requirements={"coding_required": True},
            selected_model=r.selected.to_dict() if r.selected else None,
            selected_tools=[], reasoning_level=p.reasoning_level,
            constraints={"privacy_requirement": p.privacy_requirement},
            alternatives=[m.model_id for m in r.alternatives],
            fallback_chain=[], decision_reason=r.decision_reason,
            evidence_refs=list(r.selected.evidence_refs) if r.selected else [],
            context_package_id="CTX-x", worker_id=p.worker_id)
        store.save(dec)
        loaded = store.load(dec.routing_id)
        self.assertEqual(loaded.input_hash, dec.input_hash)
        self.assertEqual(loaded.selected_model["model_id"], "m-a")
        self.assertTrue(loaded.evidence_refs)          # provenance preserved
        self.assertEqual(loaded.verification_state, "REQUESTED")  # intent, not runtime fact


class MR13_RuntimeVerification(unittest.TestCase):
    def test_MR13_route_verification(self):
        v = RouteVerifier
        self.assertEqual(v.verify("m-a", "m-a", ["t1"], ["t1"]).outcome, "MATCHED")
        self.assertEqual(v.verify("m-a", "m-b", [], []).outcome, "SUBSTITUTED")
        self.assertEqual(v.verify("m-a", None, ["t1"], ["t1"]).outcome, "PARTIAL")
        self.assertEqual(v.verify("m-a", "m-a", ["t1", "t2"], ["t1"]).outcome, "PARTIAL")
        self.assertEqual(v.verify("m-a", "m-a", ["t1"], []).outcome, "FAILED")
        self.assertEqual(v.verify("m-a", None, ["t1"], []).outcome, "UNAVAILABLE")
        # extra tool the runtime injected = SUBSTITUTED, never silently accepted
        self.assertEqual(v.verify("m-a", "m-a", ["t1"], ["t1", "t9"]).outcome, "SUBSTITUTED")


class MR14_FallbackCapabilityPreservation(unittest.TestCase):
    def test_MR14_no_capability_regression(self):
        p = profile(vision_required=True)
        r = route_models(p, [model("m-vision", caps=("vision",)),
                             model("m-cheap", caps=())])
        # cheap candidate was already rejected by the filter, so it can never
        # enter the chain:
        self.assertNotIn("m-cheap", [m.model_id for m in r.alternatives])
        # once the only capable model fails, nothing incapable may substitute
        chain = FallbackChain(p, r)
        with self.assertRaises(FallbackTriggered):
            chain.report_failure("PROVIDER_FAILURE")
        # an incapable candidate can never be reached even with a longer chain
        r2 = route_models(p, [model("m-vision", caps=("vision",)),
                              model("m-vision2", caps=("vision",))])
        chain2 = FallbackChain(p, r2)
        nxt = chain2.report_failure("TIMEOUT")
        self.assertEqual(nxt.model_id, "m-vision2")
        self.assertTrue(nxt.capabilities >= {"vision"})


class MR15_PerWorkerRouting(unittest.TestCase):
    def test_MR15_worker_routes_differ(self):
        coder = profile(worker_id="WRK-code", coding_required=True)
        vision = profile(worker_id="WRK-vision", vision_required=True)
        r_code = route_models(coder, [model("m-code", caps=("coding",)),
                                      model("m-vis", caps=("vision",))])
        r_vis = route_models(vision, [model("m-code", caps=("coding",)),
                                      model("m-vis", caps=("vision",))])
        self.assertEqual(r_code.selected.model_id, "m-code")
        self.assertEqual(r_vis.selected.model_id, "m-vis")


class MR16_ParallelRouteIsolation(unittest.TestCase):
    def test_MR16_parallel_isolation(self):
        routes = {}
        for wid, req in (("WRK-1", {"coding_required": True}),
                         ("WRK-2", {"vision_required": True}),
                         ("WRK-3", {"structured_data_required": True})):
            p = profile(worker_id=wid, **req)
            routes[wid] = route_models(p, [model("m-code", caps=("coding",)),
                                           model("m-vis", caps=("vision",)),
                                           model("m-struct", caps=("structured",))])
        self.assertEqual(routes["WRK-1"].selected.model_id, "m-code")
        self.assertEqual(routes["WRK-2"].selected.model_id, "m-vis")
        self.assertEqual(routes["WRK-3"].selected.model_id, "m-struct")
        ids = {wid: r.selected.model_id for wid, r in routes.items()}
        self.assertEqual(len(set(ids.values())), 3)     # isolated per worker


class MR17_UnknownData(unittest.TestCase):
    def test_MR17_unknown_stays_unknown(self):
        m = model("m-unk", evidence=(), lifecycle="SUPPORTED")
        self.assertIsNone(m.context_window)
        self.assertIsNone(m.cost_usd_per_1k)
        self.assertIsNone(m.latency_ms)
        self.assertEqual(m.reliability, "UNKNOWN")
        # a cost constraint with unknown cost excludes the candidate (fail-visible)
        r = route_models(profile(max_cost_usd_per_1k=0.5), [m])
        self.assertIsNone(r.selected)
        self.assertTrue(any("cost_constraint:cost_unknown" in x for x in r.rejected))


class MR18_UnavailableCandidate(unittest.TestCase):
    def test_MR18_unavailable(self):
        r = route_models(profile(), [model("m-down", available=False), model("m-up")])
        self.assertEqual(r.selected.model_id, "m-up")
        self.assertTrue(any("unavailable" in x for x in r.rejected))


class MR19_CostLatency(unittest.TestCase):
    def test_MR19_constraints(self):
        cheap = model("m-cheap", cost=0.1, latency=200)
        dear = model("m-dear", cost=2.0, latency=5000)
        r = route_models(profile(max_cost_usd_per_1k=1.0), [dear, cheap])
        self.assertEqual(r.selected.model_id, "m-cheap")
        self.assertTrue(any("cost_constraint" in x for x in r.rejected))
        r2 = route_models(profile(max_latency_ms=1000), [dear, cheap])
        self.assertEqual(r2.selected.model_id, "m-cheap")
        self.assertTrue(any("latency_constraint" in x for x in r2.rejected))


class MR20_Determinism(unittest.TestCase):
    def test_MR20_reproducible(self):
        cands = [model("m-c"), model("m-a", evidence=("e1", "e2")), model("m-b")]
        p = profile(coding_required=True)
        r1 = route_models(p, cands)
        r2 = route_models(p, list(reversed(cands)))
        self.assertEqual(r1.selected.model_id, r2.selected.model_id)
        self.assertEqual([m.model_id for m in r1.alternatives],
                         [m.model_id for m in r2.alternatives])
        d1 = RoutingDecision(task_id="T", requirements={"coding_required": True},
                             selected_model=r1.selected.to_dict(), selected_tools=[],
                             reasoning_level="MEDIUM", constraints={},
                             alternatives=[m.model_id for m in r1.alternatives],
                             fallback_chain=[], decision_reason=r1.decision_reason,
                             evidence_refs=r1.selected.evidence_refs)
        d2 = RoutingDecision(task_id="T", requirements={"coding_required": True},
                             selected_model=r2.selected.to_dict(), selected_tools=[],
                             reasoning_level="MEDIUM", constraints={},
                             alternatives=[m.model_id for m in r2.alternatives],
                             fallback_chain=[], decision_reason=r2.decision_reason,
                             evidence_refs=r2.selected.evidence_refs)
        d1.finalize(); d2.finalize()
        self.assertEqual(d1.input_hash, d2.input_hash)   # same inputs -> same decision hash


class AdversarialTests(unittest.TestCase):
    def test_capability_mismatch_primary(self):
        p = profile(vision_required=True)
        r = route_models(p, [model("m-no-vision", caps=("coding",)),
                             model("m-vision", caps=("vision",))])
        self.assertEqual(r.selected.model_id, "m-vision")   # alternate capable candidate

    def test_unverified_candidate_excluded(self):
        p = profile(reliability_requirement="VERIFIED")
        r = route_models(p, [model("m-configured", lifecycle="CONFIGURED", evidence=()),
                             model("m-verified", lifecycle="VERIFIED")])
        self.assertEqual(r.selected.model_id, "m-verified")
        self.assertTrue(any("verification_insufficient" in x for x in r.rejected))

    def test_cheap_but_incapable_fallback(self):
        p = profile(vision_required=True)
        r = route_models(p, [model("m-vision", caps=("vision",))])
        chain = FallbackChain(p, r)
        with self.assertRaises(FallbackTriggered):
            chain.report_failure("COST_CONSTRAINT")     # nothing capable left -> terminal

    def test_authority_mismatch(self):
        p = profile(tool_requirements=["shell"])
        r = route_tools(p, [ToolCandidate(tool_id="shell", type="desktop",
                                          capabilities={"shell"},
                                          verification_state="VERIFIED",
                                          evidence_refs=["e"])],
                        authority_allowed_tools=["other-tool"])
        self.assertEqual(r.selected, [])

    def test_privacy_conflict_prefers_internal(self):
        p = profile(internal_data_sufficient=True, privacy_requirement="INTERNAL_ONLY",
                    tool_requirements=["query"])
        external = ToolCandidate(tool_id="ext-search", type="web",
                                 capabilities={"query"}, verification_state="VERIFIED",
                                 evidence_refs=["e"])
        internal = ToolCandidate(tool_id="repo-grep", type="internal",
                                 capabilities={"query"}, network_required=False,
                                 verification_state="VERIFIED", evidence_refs=["e"])
        r = route_tools(p, [external, internal])
        self.assertEqual(r.selected[0], "repo-grep")

    def test_stale_current_data_source(self):
        p = profile(current_data_required=True, tool_requirements=["search"])
        stale = ToolCandidate(tool_id="old-memory", type="internal",
                              capabilities={"search"}, network_required=False,
                              verification_state="VERIFIED", evidence_refs=["e"])
        fresh = ToolCandidate(tool_id="web-now", type="web", capabilities={"search"},
                              verification_state="VERIFIED", evidence_refs=["e"])
        r = route_tools(p, [stale, fresh])
        self.assertEqual(r.selected[0], "web-now")
        self.assertTrue(any("stale_source" in x for x in r.rejected))

    def test_route_substitution_recorded(self):
        match = RouteVerifier.verify("m-requested", "m-actual", ["t1"], ["t1"])
        self.assertEqual(match.outcome, "SUBSTITUTED")
        self.assertEqual(match.actual_model, "m-actual")   # mismatch explicit


if __name__ == "__main__":
    unittest.main()
