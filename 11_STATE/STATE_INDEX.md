# STATE INDEX

## Current state
- Personal AI OS: canonical rebuild committed to GitHub.
- GitHub canonical repo: `bhaskaranjappa/personal-ai-os` (private).
- Windows clone: verified 2026-09-13 by direct inspection — synced to `origin/main` HEAD `691e277` (18 upstream commits absorbed), clean tree, disk tree == `FILE_MANIFEST.txt` (90 files at sync time), 0 broken internal file references (38 unique refs audited; only mechanism filenames named inside adapters — `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` — have no repo file by design). Pre-sync local uncommitted state preserved on branch `zcode-local-snapshot-2026-09-13`.
- Cross-platform tests executed 2026-09-13 from canonical @ `691e277` with manifest-minimum context, fresh sessions, raw outputs archived outside the repo:
  - OpenCode v1.18.29 (native CLI): CP-01..CP-06 all scored 2; G-01..G-07 all PASS.
  - Hermes v0.21.0 (CLI one-shot, OpenRouter transport, default profile model): CP-01..CP-06 all scored 2; ingestion checklist 9/9; G-01..G-05, G-07 PASS; G-06 FAIL (runtime — stale information presented as current; reproduced 2/2).
  - ZCode (GLM-5.3, OpenCode-equivalent executor per owner directive): CP-01..CP-06 all scored 2; G-01..G-07 all PASS.
  - Claude, Gemini, ChatGPT, Cursor, Codex, Claude Code, Grok: NOT_TESTED (no local runtime access from ZCode).
- Hermes: fresh runtime state captured 2026-09-13 — see `04_HERMES/HERMES_CURRENT_STATE.md`.
- B2B benchmark: completed 2026-09-05; no outreach sent. Bounded re-validation of the top candidate executed 2026-09-13 (`B2B_BENCHMARK_2026-09-13.md`) — entity-identity ambiguity preserved (six same-named companies); connectsys.co evidence recorded; outreach-ready NOT reached.

## Pending
1. ~~Verify GitHub tree and manifest.~~ DONE 2026-09-13 (tree == manifest; `PLAN(1).md` duplicate removed upstream).
2. ~~Clone/verify on Windows.~~ DONE 2026-09-13 (see above).
3. ~~Run runtime portability tests (Tier 1 available runtimes).~~ DONE 2026-09-13 for OpenCode, Hermes, ZCode-equivalent. Evidence: `12_VALIDATION/CROSS_PLATFORM_EVIDENCE_2026-09-13.md`.
4. Run remaining Tier 1 runtime tests: Claude, Gemini (blocked on owner runtime access).
5. Resolve Hermes G-06 stale-information failure (runtime-layer limitation; monitor for model/provider change; canonical layer adequate — same test passes on OpenCode and ZCode).
6. Declare V1 after release gates pass (`12_VALIDATION/V1_RELEASE_GATES.md`).
