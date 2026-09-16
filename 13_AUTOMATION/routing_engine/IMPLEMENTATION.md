# PAIOS ROUTING ENGINE — IMPLEMENTATION

Phase: V1+ Phase 10 — Model & Tool Routing
Location: `13_AUTOMATION/routing_engine/`
Language: Python 3, standard library only.
Nature: portable model/tool routing layer. Vendor-neutral: no model, provider,
coding agent, or MCP server is canonical, and no candidate carries invented
performance metrics — unknown values stay `None`/`UNKNOWN`.

## 1. Architecture position

```
Task
  -> Requirements (TaskCapabilityProfile)
  -> Capability Profile
  -> Candidate Models/Tools (registries)
  -> Evidence Filter (lifecycle/verification)
  -> Constraint Filter (authority, privacy, network, cost, latency, context)
  -> Route (deterministic selection + alternatives)
  -> Execute (runtime adapter — NOT this layer)
  -> Verify (requested vs actual)
  -> Record (RoutingDecision, durable)
```

Routing is intent, not execution. The runtime adapter decides what is actually
executable; `RouteVerifier` compares requested vs actual and records
MATCHED / PARTIAL / FAILED / SUBSTITUTED / UNAVAILABLE explicitly.

## 2. Modules

| Module | Responsibility |
| --- | --- |
| `capabilities.py` | `TaskCapabilityProfile` (all fields optional), lifecycle order, reasoning levels, vocabularies |
| `models.py` | `ModelCandidate` — capabilities, context/reasoning characteristics, cost/latency metadata (None = UNKNOWN), lifecycle, evidence refs, runtime availability |
| `tools.py` | `ToolCandidate` — type preference order (internal > connector > web > browser > desktop > user per PLAN §18), auth/permission/verification state, data sensitivity, network requirement |
| `reasoning.py` | LOW/MEDIUM/HIGH/MAXIMUM mapping from task complexity; uncertainty escalates one step, never forced |
| `router.py` | Deterministic filter → rank → select for models and tools; `route_models`, `route_tools` |
| `fallback.py` | `FallbackChain` — concrete-reason-only fallback; every step re-validated against the ORIGINAL capability contract |
| `verification.py` | `RouteVerifier` / `RouteMatch` — requested-vs-actual outcomes |
| `decisions.py` | `RoutingDecision` + durable `DecisionStore` with reproducible `input_hash` |
| `records_util.py` | utc_now, sensitivity ranking |

## 3. Task capability profile

All fields optional; absent fields impose no rule. Covers reasoning level,
context size, vision/coding/web/browser/structured/long-horizon/parallelism
requirements, latency tolerance, cost constraint, reliability requirement
(lifecycle floor), privacy requirement, tool requirements, output format, plus
two data-routing rules: `internal_data_sufficient` (internal-data-first) and
`current_data_required` (fresh external fact required).

## 4. Selection algorithm

Models — elimination order: capability mismatch → reasoning level unsupported
→ unavailable → context limit → insufficient lifecycle/verification → privacy
conflict → cost constraint → latency constraint. Ranking of survivors:
lifecycle (desc) → evidence count (desc) → model_id (asc). Deterministic;
no invented quality scores; no global "best model".

Tools — elimination: capability mismatch → network not permitted → authority
not permitted → verification below CONFIGURED → stale source when current data
required → external not needed when internal data sufficient → sensitivity
boundary. Ranking: PLAN §18 preference order → verification → evidence → id.

## 5. Fallback

Fires only on concrete reasons: TIMEOUT, PROVIDER_FAILURE, UNAVAILABLE,
CAPABILITY_MISMATCH, CONTEXT_LIMIT, COST_CONSTRAINT, LATENCY_CONSTRAINT.
Every step re-filters remaining candidates against the original profile, so a
cheaper/faster but incapable candidate can never be fallen back to. Chain
exhaustion raises `FallbackTriggered` (terminal failure, recorded).

## 6. Constraints

Authority (explicit allowed-tool list), privacy (INTERNAL_ONLY /
CONFIDENTIAL_LOCAL_ONLY forces local candidates), network (task may forbid
network), cost and latency (only configured constraints; unknown candidate
values fail visibly rather than pass silently), reliability (lifecycle floor),
capability, latency, context.

## 7. Data routing rules

Internal-data-first: when `internal_data_sufficient`, external/web tools are
rejected — canonical data is queried internally before any external research.
Current-data: when `current_data_required`, non-network sources are rejected
as `stale_source` — canonical memory is not used for present-state facts.

## 8. Provenance and decisions

`RoutingDecision` records requirements, selection, tools, reasoning level,
constraints, alternatives, fallback chain, decision reason, evidence refs,
verification state (`REQUESTED` — route intent, not runtime fact), worker and
context-package IDs, and a SHA-256 `input_hash` making the decision
reproducible from inputs. `DecisionStore` persists `RTG-*.json`. No secrets.

## 9. Runtime verification

`RouteVerifier.verify(requested_model, actual_model, requested_tools,
actual_tools)` returns MATCHED / PARTIAL / FAILED / SUBSTITUTED / UNAVAILABLE.
A runtime-substituted model or an injected extra tool is SUBSTITUTED — never
silently reported as matching.

## 10. Orchestration integration

Profiles carry `worker_id` and `context_package_id`; per-worker routes are
independent (MR-15/MR-16): parallel workers on one workflow legitimately
receive different model/tool routes. Routing is performed against the task's
selected context, not the whole repository.

## 11. Extension points

- Registry persistence: registries are in-memory lists today; a durable
  registry store (like DecisionStore) is a straightforward addition when a
  real candidate population justifies it.
- Semantic capability matching: capability vocabularies are exact-token sets.
- Runtime adapters declare what is executable; none exists yet — that is the
  next phase activity, not a claim made here.

## 12. Tests

`tests/test_phase10.py` — 27 tests: MR-01..MR-20 + 7 adversarial cases
(capability mismatch, unverified candidate, cheap-but-incapable fallback,
authority mismatch, privacy conflict, stale current-data source, route
substitution).
Run: `cd 13_AUTOMATION/routing_engine && python -m unittest tests.test_phase10 -v`
