# ZCode-Class Runtime Adapter — Codex CLI (`zcode_adapter.py`)

The first REAL runtime adapter in PAIOS. Implements the Phase 13
`RuntimeAdapter` contract around the actually installed OpenAI Codex CLI.
Nothing in this adapter infers a capability that was not directly observed.

## Discovered runtime boundary (all directly observed 2026-09-17)

| Fact | Evidence |
|---|---|
| Executable | `codex` → `C:\Users\ABhas\AppData\Roaming\npm\codex.CMD` (npm `@openai/codex` 0.144.1) |
| Entry point | `codex exec --skip-git-repo-check -m <model> -s <sandbox> [-C <dir>]`, prompt via stdin |
| Auth | ChatGPT-account mode (`~/.codex/auth.json`, `auth_mode: "chatgpt"`) |
| Working model | `gpt-5.5` (from `~/.codex/models_cache.json` roster). Configured default `gpt-5.4-mini` is rejected by the account tier (400 invalid_request_error, observed repeatedly across many model-slug probes) |
| Output | plain mode: final agent message printed (duplicated tail); `--json`: JSONL event stream (`item.completed` / `agent_message`, `turn.completed` / usage) |
| Exit codes | 0 on success; 1 with ERROR lines on API/model failure; external SIGKILL → 124 |
| Sandbox | `-s read-only` VERIFIED honored: a write request produced the proposed command but did NOT modify the target file |
| Working dir | `-C <dir>` VERIFIED: task isolated to the given directory |
| Timeout | externally enforceable; 1s deadline observed → exit 124, no output |
| Session | rollout JSONL files written under `~/.codex/sessions/…` with session ids |

## Adapter design

`CodexRuntimeAdapter(RuntimeAdapter)`:

- `health()` — AVAILABLE when the binary exists (auth state observable via auth.json)
- `execute(request)` — builds the runtime prompt from the canonical request
  (task id, authority context as **informational data**, objective,
  acceptance criteria, task prompt), invokes `codex exec` with the resolved
  model/sandbox/workspace, parses the result, and normalizes:
  - process error lines / nonzero exit → `FAILED` (with surfaced error message)
  - deadline exceeded → `TIMEOUT` (never success)
  - exit 0 with no agent message → `UNKNOWN` (never success)
  - agent message present → `COMPLETED` with evidence refs
- `verify(result)` — well-formedness + untrusted-output inspection; FAILED/UNKNOWN never verify
- `check_acceptance(request, result)` — structural criteria check; the
  orchestration layer supplies semantic criterion checks
- cancellation — inherited `cancel()` raises: not supported by this boundary (honest)

A successful process exit is never equated with task success.

## Verification model

Statuses map to the Phase 13 contract: `COMPLETED / FAILED / UNKNOWN / TIMEOUT`.
The result carries: execution id, runtime id (`codex-cli`), adapter id,
request fingerprint, timestamps, output ref (agent message), evidence refs
(session-output, model, exit code), error, and a verification dict
(exit code, model, sandbox, usage where the stream provides it).

## Honest limitations

- Only `gpt-5.5` has been verified live; other model slugs are unverified.
- Usage/token metadata is only parsed in `--json` mode (plain mode records none).
- No streaming, no parallelism, no background execution, no cancellation.
- The account-tier model restriction means the adapter pins a verified model
  rather than the configured default; substitution of models by the runtime
  was not observed and none is claimed.
