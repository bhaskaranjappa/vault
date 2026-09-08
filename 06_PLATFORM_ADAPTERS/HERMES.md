# HERMES ADAPTER

## Purpose
Consume the Personal AI OS without duplicating canonical knowledge.

## Native ingestion
- Hermes should read the canonical repository through its available file/repository tools or GitHub CLI integration.
- Use the repository's manifest and task routing rules to select minimum relevant context.
- For the current environment, live GitHub repository access through the bundled GitHub skill and `gh` CLI is the established integration path.

## Minimum context
Use the manifest-defined task package rather than dumping the complete Personal AI OS into Hermes memory.

## Rules
- Canonical OS is the source of truth.
- Preserve status states and BRUTALIST rules.
- Do not silently overwrite canonical knowledge.
- Do not treat Hermes memory, skills, or runtime configuration as canonical project truth.
- Do not claim capability or parity without runtime evidence.

## Verification status
- GitHub CLI live-repository access: previously verified in local runtime audit; current-session recheck NOT_TESTED.
- Canonical context ingestion from live `main`: NOT_TESTED in a fresh session.
- CP-01 through CP-06: NOT_TESTED.

Reference:
- `04_HERMES/HERMES_CURRENT_STATE.md`
- `12_VALIDATION/LIVE_HERMES_RUNTIME_CHECK.md`