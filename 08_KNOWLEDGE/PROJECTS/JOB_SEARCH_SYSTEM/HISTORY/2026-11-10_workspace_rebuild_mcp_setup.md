# Historical Session Summary — 2026-11-10 Workspace Rebuild and MCP Setup

**Source:** user-provided attachment `Pasted text(20261110-063647).txt`  
**Capture date:** 2026-11-10  
**Provenance:** original user-provided summary, preserved at full length below.  
**Privacy:** direct email addresses have been redacted in this public VAULT copy. The full source-preserved version is retained in private JOBS `MEMORY.md`.

> Historical snapshot. Its 66-row tracker, open tasks and tool-state claims are superseded where newer evidence exists. Consult JOBS `MEMORY.md`, `00-tracking.csv` and current Gmail evidence before acting.

---

---
## CONTEXT: Building a human-in-the-loop job-search outreach pipeline for Bhaskar Anjappa (GenAI Engineer, India) targeting YC startups — job discovery → founder email enrichment → cold-email drafting → manual send. This thread's work: restructuring the workspace and installing/configuring an email-enrichment MCP stack across five coding agents.

## STACK / ENVIRONMENT
- **User**: Bhaskar Anjappa, Generative AI Engineer, 3+ yrs, India-based. Resume email [REDACTED_EMAIL]`.
- **Links (locked signature)**: GitHub `https://github.com/bhaskaranjappa` | HF `https://huggingface.co/BhaskarAnjappa` | LinkedIn `https://www.linkedin.com/in/bhaskar-anjappa-9070a2318`
- **Stack**: Python, LangGraph, LangChain, LlamaIndex, FastAPI, Milvus, PyTorch, Docker, GCP Vertex AI, LangSmith, n8n/Make.com, Gemini (Vertex AI)
- **OS/shell**: Windows, PowerShell 7.6.9. Node v26.12.1, Python 3.14.
- **Workspace**: `C:\Users\ABhas\projects\jobs`
- **Coding agents used**: Antigravity, OpenCode, ZCode, Freebuff (web), DeepSeek Harness.
- **MCP servers**: `yc-mcp-connector` / `workatastartup-mcp` (job search), `apollo-mcp` (enrichment, credit-limited), `prospector-mcp` (new — Apollo replacement, 5 tools: `usage_stats`, `check_domain`, `verify_email`, `verify_emails_batch`, `find_emails`).
- **CLI tools**: `coldreach` installed (`C:\Users\ABhas\AppData\Roaming\Python\Python314\Scripts\coldreach.exe`, PATH fixed), `freebuff-mcp` 0.2.7 installed (bridge — abandoned), `mcpsmgr` 0.3.0 (upgrade to 0.4.9 failed, abandoned), `mcpman` (installed but useless — supports none of user's agents).

## WHAT'S BEEN DONE

**1. Workspace wiped and rebuilt.** Antigravity had produced a research dump (25 companies, 28 jobs, 57 source URLs). All deleted except 6 keepers moved to `_reference/`:
`source_register.csv`, `jobs_ranked.csv`, `jobs_ranked.json`, `founder_contacts.csv`, `founder_research.md`, `final_report.md`.
Final structure:
```
jobs/
├── 00-tracking.csv   (66 rows: 38 SENT, 28 NOT_SENT)
├── 01-notes.md       (locked email template, project mapping, confidence taxonomy, status vocabulary)
├── README.md
├── drafts/           (empty)
└── _reference/       (6 files, read-only archive)
```

**2. CSV corruption fixed.** Initial write produced mixed column counts (29×9, 32×8, 5×10 — emails landed in `founder` slot, unquoted commas in notes). Fixed via Python `csv` module with `QUOTE_ALL`. Schema locked:
`company,role,founder,email,confidence,date_sent,followup_due,status,notes`

**3. Prospector-mcp installed and verified across 3 of 5 agents:**

| Agent | Config path | Key shape | Status |
|---|---|---|---|
| Antigravity | `~/.gemini/config/mcp_config.json` | `mcpServers`, command string + args array, `cmd /c npx` | ✅ connected |
| OpenCode | `~/.config/opencode/opencode.json` | `mcp`, `"type":"local"`, command as **array** | ✅ connected |
| ZCode | `~/.zcode/cli/config.json` | `mcp.servers`, command as **string** + args array | ✅ connected (merged into existing config with `codegraph` + `node_repl`; backup at `.bak`) |
| Freebuff (web) | — | browser cannot reach localhost | ❌ not possible |
| DeepSeek Harness | — | no `mcpServers` JSON exists | ❌ skipped |

**4. Email verification run — real results written to CSV:**

| Email | Verdict | Score | Catch-all | CSV action |
|---|---|---|---|---|
| [REDACTED_EMAIL]` | valid | 95 | false | → `VERIFIED` |
| [REDACTED_EMAIL]` | valid | 95 | false | → `VERIFIED` (was LOW_GUESSED pattern) |
| [REDACTED_EMAIL]` | valid | 95 | false | → `VERIFIED` |
| [REDACTED_EMAIL]` | risky | 50 | **true** | stayed `LOW_GUESSED`, note updated |
| [REDACTED_EMAIL]` | risky | 50 | **true** | stayed `LOW_GUESSED`, note updated |
| [REDACTED_EMAIL]` | risky | 50 | **true** | stayed `LOW_GUESSED`, note updated |
| [REDACTED_EMAIL]` | risky | 50 | **true** | stayed `FOUND_UNVERIFIED`, note updated |
| [REDACTED_EMAIL]` | risky | 50 | **true** | stayed `FOUND_UNVERIFIED`, note updated |

**Critical finding:** 5 of 8 domains are catch-all. For Flock Safety, AIOS, Standout — **a bounce will never arrive** even if the pattern was wrong. Old "wait 24–48h for bounce" plan is dead for those three. New rule: 5-day no-reply → assume wrong → LinkedIn DM.

**5. FirstWork draft produced and QC'd.** Original had 4 failures (4-line middle paragraph, no gap clause, invented "50,000 workers a week" stat not in JD, "validate credentials" inferred). Rewritten version (user declined to apply further edits, said "let it be that's not a problem"). **Draft was never sent.**

## CURRENT STATE / PROBLEM
- Tool install thread is **complete**. No further installs needed. `find_emails` is the only prospector tool never called.
- `00-tracking.csv` is structurally valid, 66 rows, confidence counts correct.
- **All 66 rows have empty `date_sent` and `followup_due`** — blocks all Day-5 follow-up logic.
- **`find_emails` untested** — Apollo-replacement fallback is theoretical until proven.
- **FirstWork email drafted but unsent** — [REDACTED_EMAIL]` is SMTP-verified, fit 5, remote-from-India.
- 4 `LOW_GUESSED` addresses (Flock Safety, Runtime, AIOS, Standout) — Runtime now VERIFIED, other three catch-all.

## KEY DECISIONS + WHY
- **Human sends every email.** Automation covers discovery + enrichment + drafting only. Avoids bot detection, Apollo ToS violation, account ban.
- **Apollo official API only, no browser automation.** ToS prohibits automated extraction.
- **Prospector replaces Apollo when credits run out** — free, 50/day, SMTP-verified, no fabricated confidence scores (Apollo's earlier run emitted fake 97%/100% scores which Apollo does not produce).
- **`mcpman` and `mcpsmgr` abandoned.** `mcpman` supports none of user's five agents. `mcpsmgr` stuck at 0.3.0, upgrade to 0.4.9 failed. Manual JSON config is faster.
- **Freebuff MCP bridge abandoned.** Desktop requires opening a local clone of a remote Git repo to unlock local syncing; user uses Freebuff web instead. Web cannot host MCP.
- **Local models dropped.** 14B on CPU = 5–15 tok/s, 10–30s per response; agent loops make 5–15 sequential calls, KV cache spill collapses speed further. Not viable for agent work.
- **WaaS MCP (`github.com/Thespaceblade/waas-mcp`) rejected.** Its unique features are all application-side (`inspect_application`, `application_quota`, profile tools); pipeline doesn't apply through WaaS. Requires Playwright + persisted signed-in session — conflicts with no-credentials-to-agents rule.
- **Never use `github.com/yc-software/waas-mcp`** — recruiter-side, wrong tool.
- **Fit scores from Antigravity inflated** (94–98). Re-scored: GetCrux 5→4, Voiceops 4→3, Cardboard 3/5.

## OPEN THREADS / NEXT STEPS
1. **`find_emails` test** — the immediate next action. Run in Antigravity: `Use prospector's find_emails tool on domain "getcrux.ai" with contact name "Atharva Padhye"`. GetCrux is founder-name-confirmed, email `NOT_FOUND`. Costs 3–8 of 50 daily credits. Result determines whether Apollo fallback is real or whether all `NOT_FOUND` rows go straight to LinkedIn DM.
2. **Populate `date_sent`** for 38 SENT rows from Gmail sent folder — blocks Day-5 follow-ups.
3. **Send the FirstWork email** — verified address, rewritten draft ready.
4. **Bounce/follow-up handling** — three catch-all domains will never bounce; 5-day no-reply = LinkedIn DM.
5. **OpenOutreach vs Apollo A/B test** — 20-credit cap, designed, never run.
6. **Re-verify stale listings**: Karumi (posted 2025-12-04), Dart (2025-04-19), Hera (2025-10-18).
7. [REDACTED_EMAIL]`** — last remaining `VERIFIED_DATABASE` row, never checked.

## DO NOT
- Do not write emails longer than 2–3 lines in the middle paragraph.
- Do not include "I recently applied for [role] at [company]" — user removed this twice.
- Do not include multiple projects in one email.
- Do not invent/guess email addresses or statistics not in the JD (the "50,000 workers" failure).
- Do not send or submit automatically — human approval on every send.
- Do not resend to a BOUNCED address — LinkedIn DM only.
- Do not re-suggest local models, `mcpman`, `mcpsmgr`, Freebuff MCP bridge, WaaS MCP, or Freebuff Desktop — all evaluated and rejected.
- Do not suggest ARTEMIS (Android-only), Lightpanda (rendering only), Chrome DevTools MCP (debugging only).
- Do not enable OpenOutreach `send`/`run`.
- Do not respond in Chinese — English only.
- Do not add project lists, tool inventories, or skill dumps to outreach emails.
- Do not paste prose paths into PowerShell expecting them to open — use `notepad <path>` or `Get-Content`.

## LOCKED EMAIL FORMAT (verbatim, never paraphrase)
```
**To:** [email]
**Subject:** [6–10 words, specific to product/role]

Hi [First Name],

I'm a GenAI engineer with 3+ years of experience building production LLM, RAG and AI-agent systems with Python, FastAPI, LangGraph, Docker and modern LLM APIs.

[2–3 lines ONLY: specific JD problem + ONE project that maps to it.]

I'd welcome a short conversation if there's a fit.

Best,
Bhaskar Anjappa
GitHub: https://github.com/bhaskaranjappa
Hugging Face: https://huggingface.co/BhaskarAnjappa
LinkedIn: https://www.linkedin.com/in/bhaskar-anjappa-9070a2318
```

## PROJECT → JD MAPPING (pick exactly ONE)
| JD theme | Project |
|---|---|
| RAG/retrieval/document search | Enterprise RAG & Knowledge Base (Milvus hybrid + cross-encoder reranking, FastAPI, Groq/Llama 3.3 70B on HF Spaces) |
| Agents/orchestration | Deep Research Multi-Agent System (LangGraph planner–researcher–writer, cyclic critique) |
| Research/model fundamentals | Transformer-Based LLM from Scratch (PyTorch, multi-head attention, custom tokenization) |
| Serving/APIs/deployment | FastAPI services with auth, rate limiting, tracing + LangSmith |
| Automation/internal tools | 10+ n8n/Make LLM-integrated workflows |
| Summarization/classification | Gemini pipelines on Vertex AI |

## CONFIDENCE TAXONOMY (locked)
`VERIFIED` (SMTP or Apollo-confirmed) · `VERIFIED_PUBLIC_COMPANY` (founders@/hello@/contact@ on company site) · `VERIFIED_DATABASE` (scraped directory — spot-check) · `FOUND_UNVERIFIED` (personal site/paper/GitHub — spot-check) · `LOW_GUESSED` (pattern inference, may bounce) · `NOT_FOUND` (LinkedIn DM only)

## STATUS VOCABULARY (locked)
`SENT` · `NOT_SENT` · `FOLLOWUP_DUE` · `FOLLOWUP_SENT` · `BOUNCED` · `REPLIED` · `CLOSED`

---

