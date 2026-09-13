# HERMES VERSIONS

Current recorded version: 0.21.0 (verified by fresh runtime audit 2026-09-13 on the owner's Windows machine; `hermes --version` → "Hermes Agent v0.21.0 (2026.8.31) · upstream 04b88a4c · local 63279301 (+1 carried commit)"). Previous entry: "verified by prior runtime audit" — superseded.

Build details captured 2026-09-13:
- OS: Windows
- Install method: git
- Python: 3.11.16
- OpenAI SDK: 2.24.0
- Config version: v40 (up to date per `hermes doctor`)

Default profile model: `gemini-2.5-flash-lite` (Google AI Studio) — historical Nemotron / Solar Pro 4 records remain provenance.

Transport limitation: Google AI Studio direct endpoint fails in one-shot mode (HTTP 302); OpenRouter transport works (`--provider openrouter -m google/gemini-2.5-flash-lite`). OpenRouter free tier cannot fund `google/gemini-2.5-flash` (HTTP 402).

Skills: 53 enabled — 51 builtin + 2 local; 0 hub-installed; 0 disabled.

MCP: no servers configured.
Cron: no scheduled jobs.
Gateway: not running.
Memory: built-in enabled (injection + user profile).
Plugins: a2a enabled; browser-browser-use v1.0.0 disabled.

Reverification rule: update this file from fresh runtime evidence when local state changes.