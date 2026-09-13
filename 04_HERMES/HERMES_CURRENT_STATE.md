# HERMES CURRENT STATE

Last full runtime capture: 2026-09-13 (CLI inspection on the owner's Windows machine; `hermes --version`, `status`, `doctor`, `profile list`, `skills list`, `mcp list`, `cron list`, `gateway status`, `memory status`, `plugins list`). Supersedes the prior audit below where they differ.

## Fresh verified state — 2026-09-13
- Version: 0.21.0 (2026.8.31), upstream 04b88a4c, local 63279301 (+1 carried commit); install method git; Python 3.11.16; OpenAI SDK 2.24.0.
- OS: Windows; CLI launches and executes one-shot (`-z`) and state subcommands.
- Default profile (`default`): model `gemini-2.5-flash-lite`, provider Google AI Studio.
- API keys present: OpenRouter (configured), Google/Gemini (configured). Not set: OpenAI, Anthropic, xAI, NVIDIA, GitHub, Firecrawl, Tavily, and others per `hermes status`.
- Nous Portal: logged in, but inference access expiry shown as 2026-09-08 16:12 IST (expired at capture time).
- Google AI Studio direct endpoint FAILED in one-shot mode (HTTP 302 after retries). OpenRouter transport works (`--provider openrouter -m google/gemini-2.5-flash-lite`). OpenRouter free tier cannot fund `google/gemini-2.5-flash` (HTTP 402); flash-lite is the working model.
- Skills: 53 enabled — 51 builtin + 2 local, 0 hub-installed, 0 disabled.
- MCP: no servers configured.
- Cron: no scheduled jobs.
- Gateway: not running.
- Memory: built-in (MEMORY.md/USER.md) enabled; memory injection enabled; user profile enabled.
- Plugins: a2a enabled (bundled); browser-browser-use v1.0.0 disabled (bundled).
- Doctor: config v40 up to date, no deprecated keys, no security advisories, SSL bundle valid, SQLite WAL healthy; optional python-telegram-bot / discord.py not installed; OpenAI Codex auth and MiniMax OAuth not logged in.
- One-shot runtime behavior: `--in DIR` not honored in `-z` mode (two failed ingestion attempts); file/terminal tools function when absolute paths are given in the prompt with `-t file,terminal --yolo`.
- Behavioral evidence: CP-01..CP-06 all scored 2 from fresh sessions; governance G-01..G-05/G-07 PASS; G-06 FAIL reproduced 2/2 (stale information presented as current — runtime/model-layer limitation; canonical rules adequate, same test passes on OpenCode and ZCode). Evidence: `12_VALIDATION/CROSS_PLATFORM_EVIDENCE_2026-09-13.md`.

## Historical — prior audit (retained for provenance)
- Desktop installed; CUA driver installed and functional; local execution backend active; delegation enabled; LSP framework present (server binaries unverified on PATH); MoA framework present not enabled; checkpoint infrastructure present (requirement disabled); a2a was the only enabled plugin toolset; 51 built-in skills, no local/hub skills; no MCP servers; no cron jobs; Google/Groq/NVIDIA keys and messaging auth not established as verified.

## Model state
Default profile model is `gemini-2.5-flash-lite` (Google AI Studio) as of 2026-09-13. The historical Nemotron → Solar Pro 4 records remain provenance. The default Google-direct inference endpoint currently fails (HTTP 302) in one-shot mode; OpenRouter is the working transport.

## Rule
Update this file from fresh runtime evidence when local state changes.
