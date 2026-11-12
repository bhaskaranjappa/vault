# Historical Session Summary — 2026-11-12 Campaign and Enrichment Work

**Source:** user-provided attachment `Pasted text(20261112-055744).txt`  
**Capture date:** 2026-11-12  
**Provenance:** original user-provided summary, preserved at full length below.  
**Structure:** contains two separate `CONTEXT` sections in the same attachment. Both are retained in order.  
**Privacy:** direct email addresses have been redacted in this public VAULT copy. The full source-preserved version is retained in private JOBS `MEMORY.md`.

> Historical snapshot. The 29-company and 23-company campaign cohorts describe different runs. Do not merge their counts. The current operational tracker in the private JOBS repository is authoritative.

---

---
## CONTEXT: Job-search outreach pipeline for Bhaskar Anjappa (GenAI Engineer, India) targeting YC startups — building a human-in-the-loop automation system for job discovery, founder email enrichment, and cold-email drafting.

## STACK / ENVIRONMENT
- **User profile**: Bhaskar Anjappa, Generative AI Engineer, 3+ yrs, India-based. Resume email [REDACTED_EMAIL]` (Apollo record shows [REDACTED_EMAIL]` — use [REDACTED_EMAIL]` to match resume/LinkedIn).
- **Links (fixed signature block)**: GitHub `https://github.com/bhaskaranjappa` | Hugging Face `https://huggingface.co/BhaskarAnjappa` | LinkedIn `https://www.linkedin.com/in/bhaskar-anjappa-9070a2318`
- **Stack**: Python, LangGraph, LangChain, LlamaIndex, FastAPI, Milvus, PyTorch, Docker, GCP Vertex AI, LangSmith, n8n/Make.com, Gemini (Vertex AI)
- **MCP servers in use**: `workatastartup-mcp` / `yc-mcp-connector` (job search; supports `remote` and `visa` boolean filters separately — do not combine); `apollo-mcp` (people enrichment); WaaS MCP `github.com/Thespaceblade/waas-mcp` (candidate-side: `waas_search`, `waas_get_job`, `waas_get_company`, `waas_inspect_application`, `waas_submit_application` with `dry_run:true` default, `waas_application_quota`). **Do not use** `github.com/yc-software/waas-mcp` — that is recruiter-side.
- **Other tools**: Freebuff with OpenOutreach + 11 skills installed; coding agents opencode/zcode/DeepSeek Harness/Antigravity.
- **Note**: `get_job_details` and `get_company_details` do not exist as named tools — fetch job by job_id and company by company_id via search.

## WHAT'S BEEN DONE

**1. Strategy decided — human-in-the-loop pipeline (3 layers):**
- Layer 1: YC MCP agent searches jobs + extracts founders → structured lead table
- Layer 2: Apollo MCP agent enriches founder emails (official API only)
- Layer 3: Drafting agent writes one email per founder → **user reviews and manually sends from Gmail**
- Rationale: browser automation of submit/send fails on CAPTCHA/bot detection and violates Apollo ToS (explicitly prohibits automated extraction; risk of rate-limit/ban).

**2. Email format finalized (locked — use verbatim):**
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
Hard rules: no "I recently applied for…" line; middle paragraph 2–3 lines max; name the specific JD problem; exactly ONE proof project; state gaps honestly in one clause; no placeholders; never invent emails; drafts only.

**3. Project→JD mapping table (for picking proof project):**
| JD theme | Project |
|---|---|
| RAG/retrieval/document search | Enterprise RAG & Knowledge Base (Milvus hybrid + cross-encoder reranking, FastAPI, Groq/Llama 3.3 70B on HF Spaces) |
| Agents/orchestration | Deep Research Multi-Agent System (LangGraph planner–researcher–writer, cyclic critique) |
| Research/model fundamentals | Transformer-Based LLM from Scratch (PyTorch, multi-head attention, custom tokenization) |
| Serving/APIs/deployment | FastAPI services with auth, rate limiting, tracing + LangSmith |
| Automation/internal tools | 10+ n8n/Make LLM-integrated workflows |
| Summarization/classification | Gemini pipelines on Vertex AI |

**4. Applied list — 29 companies/roles (all emails sent):**
1. Infer — Applied AI Engineer 2. Crustdata — Founding ML Engineer (India) 3. Narrative — Founding Engineer (Backend + AI) 4. Lab0 — Forward Deployed Engineer 5. kapa.ai — Research Engineer, Applied AI 6. NewsCatcher — Software Engineer (Backend & LLM) 7. Zudo — Forward-Deployed Engineer, AI Agents 8. Peakflo — Technical Ops & AI Automation Engineer 9. Datrics — AI Engineer 10. AnswerThis — Product Engineer 11. Opusense AI — Software Engineer 12. Synthio Labs — Software Engineer – AI 13. Rollstack — AI Software Engineer 14. Asha Health — Staff SWE, AI Agents 15. Plexe — Forward Deployed Engineer 16. Leeroo — Founding Engineer 17. LFcarry — AI Product Engineer 18. Reducto — LLM/ML Engineer (Inference) 19. arnata — AI Engineer 20. Unsiloed AI — Founding ML Researcher 21. ClaimSorted — AI Engineer 22. Stilta — AI Engineer 23. Solve Intelligence — AI Engineer 24. Clara — Founding AI Engineer 25. Flock Safety — Staff AI Systems Engineer 26. Runtime — Forward Deployed AI Engineer 27. AIOS — AI Engineering Lead 28. Standout — Founding AI Product Engineer 29. Salus — Founding SWE/MLE (email to Vedant)

**5. Email addresses by confidence:**
- HIGH: [REDACTED_EMAIL]` (LFcarry), [REDACTED_EMAIL]` (Reducto), [REDACTED_EMAIL]` (arnata), [REDACTED_EMAIL]` (Unsiloed), [REDACTED_EMAIL]` (ClaimSorted), [REDACTED_EMAIL]` (Stilta)
- MEDIUM (general inbox): [REDACTED_EMAIL]` (Solve), [REDACTED_EMAIL]` (Clara)
- LOW/GUESSED (sent, watch bounces): [REDACTED_EMAIL]`, [REDACTED_EMAIL]`, [REDACTED_EMAIL]`, [REDACTED_EMAIL]`
- Earlier verified batch (21 emails) from Apollo: kapa.ai ([REDACTED_EMAIL]`), Peakflo ([REDACTED_EMAIL]`), Datrics ([REDACTED_EMAIL]`, [REDACTED_EMAIL]`), AnswerThis ([REDACTED_EMAIL]`, [REDACTED_EMAIL]`), NewsCatcher ([REDACTED_EMAIL]`, [REDACTED_EMAIL]`), Opusense ([REDACTED_EMAIL]`, [REDACTED_EMAIL]`), Synthio (`raj@`, `sahityas@`, [REDACTED_EMAIL]`), Rollstack (`nabil@`, `saad@`, [REDACTED_EMAIL]`), Asha ([REDACTED_EMAIL]`), Plexe ([REDACTED_EMAIL]`), Leeroo ([REDACTED_EMAIL]`, [REDACTED_EMAIL]`)

**6. Second Apollo run on 22 new founders (Tiers 1–3, 14 non-deferred):** 0 VERIFIED, 1 CATCH_ALL (LFcarry [REDACTED_EMAIL]`), 13 NOT_FOUND. Notes said "Apollo person record confirmed. No email on file." — coverage gap, not prompt failure. **Flagged: Apollo emitted "GUESSED" rows with fabricated confidence scores (97%/100%) — Apollo does not produce these; treat as unverified pattern inference.**

## CURRENT STATE / PROBLEM
- All 29 applications/emails sent. 4 low-confidence guessed addresses (Flock Safety, Runtime, AIOS, Standout) may bounce — monitor 24–48h.
- 2 general-inbox sends (Solve Intelligence, Clara) will have low reply rate — LinkedIn follow-up after 5 days.
- **OpenOutreach vs Apollo A/B test is proposed but results not returned.** Test design: 20-credit cap on BetterContact, no `send`/`run`, Step 2 = independently verify Apollo's 4 guesses using free web/LinkedIn skills, Step 5 = enrich max 20 credits, output comparison table with EXACT/DIFFERENT_VERIFIED/OA_ONLY/APOLLO_ONLY/BOTH_MISS verdicts.
- YC agent was given a prompt to find 22 new leads (excluding the 29 applied) with `remote=true` and `visa=true` as separate queries — that output is what fed the second Apollo run.

## KEY DECISIONS + WHY
- **Human sends the final email** — avoids bot detection, Apollo ToS violation, and account ban. Automation covers discovery + enrichment + drafting only.
- **Apollo official API only, no browser automation** — ToS explicitly prohibits automated extraction.
- **Do not give login credentials to ChatGPT/agents** — a signed-in agent has full account access; security risk.
- **Email format: 2–3 line middle paragraph, no "I recently applied" line** — user corrected this twice; do not reintroduce either.
- **Project mapping picks ONE project per email** — user rejected multi-project listing as over-long.
- **OpenOutreach `send` never enabled** — it is a B2B sales tool; sales tone damages personal sender reputation in job-search context.
- **Tier 4 companies skipped** (Respan, Dill, ShipBob, Luca IQ, Intryc, 83 Sciences, Fieldguide, PostEra, Saphira AI, Hirebolt) — require existing US work authorization Bhaskar does not have.

## OPEN THREADS / NEXT STEPS
1. **OpenOutreach A/B test verdict** — run the 20-credit-capped prompt, return comparison table, decide: replace Apollo / keep both / drop OpenOutreach.
2. **Follow-up emails Day 5** on all non-responders. Template: subject `Re: [same subject]`, short "just following up — happy to share a Loom walkthrough" + CTA.
3. **Bounce handling** — for any bounced guessed address, switch to LinkedIn DM, do not resend.
4. **Tracking sheet still needs to exist**: Company | Founder | Email used | Confidence | Date sent | Follow-up date (Day 5) | Status.
5. **New YC lead search** if user wants more targets — reuse the exclusion prompt with the 29 applied names.

## DO NOT
- Do not write emails longer than 2–3 lines in the middle paragraph.
- Do not include "I recently applied for [role] at [company]" — explicitly removed by user.
- Do not include multiple projects in one email.
- Do not invent/guess email addresses ([REDACTED_EMAIL]`) — mark NOT_FOUND instead.
- Do not send or submit automatically — human approval on every send.
- Do not use `github.com/yc-software/waas-mcp` (recruiter-side, wrong tool).
- Do not suggest ARTEMIS (Android-only), Lightpanda (rendering layer only), or Chrome DevTools MCP (debugging only) — all evaluated and rejected as not fitting this workflow.
- Do not enable OpenOutreach `send`/`run`.
- Do not respond in Chinese — English only.
- Do not add project lists, tool inventories, or skill dumps to outreach emails.

---
## CONTEXT: Building a human-in-the-loop job-search outreach pipeline for Bhaskar Anjappa (GenAI Engineer, India) targeting YC startups. This thread covers exhaustive scraping/enrichment tool testing (Agent-Reach, Apollo, Firecrawl, Scrapling, Prospector) and finalizing a 23-company hybrid email list for drafting and manual send.

## STACK / ENVIRONMENT
- **User**: Bhaskar Anjappa, Generative AI Engineer, 3+ yrs, India-based.
- **OS/Shell**: Windows, PowerShell 7.6.9. Python 3.14. Node v26.12.1.
- **Workspace**: `C:\Users\ABhas\projects\jobs`
- **Coding Agents**: Antigravity (primary), ZCode, OpenCode.
- **Tools tested/used**: 
  - `agent-reach` (CLI/Skill): Primary discovery tool (25/25 success).
  - `prospector` (MCP): SMTP verification (1 credit remaining, resets daily).
  - `apollo.io` (API): Found 24 emails manually, but emitted incorrect domains.
  - `scrapling` (CLI): Rendered LinkedIn but yielded no emails.
  - `firecrawl` / `coldreach`: Dropped. Failed on Apollo/LinkedIn and DNS timeouts, respectively.

## WHAT'S BEEN DONE
**1. Scraping Capability Matrix Finalized:**
- **Apollo.io**: Hard-blocked (HTTP 410 `fault filter abort` via Cloudflare).
- **LinkedIn**: Auth-walled (HTTP 999). No unauthenticated email extraction possible.
- **Agent-Reach**: The only working discovery tool. Found 25/25 addresses via YC launches, GitHub, and company pages.
- **Prospector**: Verified 6 addresses with SMTP 95.

**2. Hybrid Email List Generated:**
- Cross-referenced Agent-Reach's verified company domains (fixing Apollo's hallucinations like `itsdart.com`) with Apollo's personal founder emails (e.g., [REDACTED_EMAIL]`).
- Excluded Rex `careers@` (application intake) and GovernGPT `support@` (support queue).

**3. Final 23-Company Hybrid List Locked:**
```text
1. Juno | Marshall Gould | [REDACTED_EMAIL]
2. FirstWork | Vardhan Kapoor | [REDACTED_EMAIL]
3. Karumi | Pablo Omenaca | [REDACTED_EMAIL]
4. Voiceops | Ethan Barhydt | [REDACTED_EMAIL]
5. GetCrux | Atharva Padhye | [REDACTED_EMAIL]
6. Strac | Aatish Mandelecha | [REDACTED_EMAIL]
7. Zymbly | Ben Jacob | [REDACTED_EMAIL]
8. mdhub | Dominik Middelmann | [REDACTED_EMAIL]
9. Guac | Euro Wang | [REDACTED_EMAIL]
10. Openbenchmarks | Aditya Lahiri | [REDACTED_EMAIL]
11. Dart | Milad Malek | [REDACTED_EMAIL]
12. Tavus | Hassaan Raza | [REDACTED_EMAIL]
13. Rudus | Sahil Goel | [REDACTED_EMAIL]
14. Dime | Akash Kumar | [REDACTED_EMAIL]
15. Allus AI | Kai Cui | [REDACTED_EMAIL]
16. Moss | Sri Raghu Malireddi | [REDACTED_EMAIL]
17. Silimate | Akash Levy | [REDACTED_EMAIL]
18. Hera | Peter Tribelhorn | [REDACTED_EMAIL]
19. telli | Seb Hapte-Selassie | [REDACTED_EMAIL]
20. Zeit AI | Leopold von Waldthausen | [REDACTED_EMAIL]
21. Cardboard | Ishan Sharma | [REDACTED_EMAIL]
22. Flair Labs | Samir Sen | [REDACTED_EMAIL]
23. CTGT | Cyril Gorlla | [REDACTED_EMAIL]
```

## CURRENT STATE / PROBLEM
- The final 23-row hybrid list is locked.
- The drafting prompt for the YC agent is written and ready to be executed.
- **Blocker**: `00-tracking.csv` still has 38 rows marked `SENT` with empty `date_sent` fields, breaking all Day-5 follow-up logic.

## KEY DECISIONS + WHY
- **No more tool testing**: Apollo and LinkedIn are un-scrapable by this stack. Firecrawl and Coldreach are dropped.
- **Hybrid Data Strategy**: Used Agent-Reach for verified domains and Apollo for personal email formats.
- **Drafting via YC Agent**: The YC agent holds the JD context, so it must be the one to draft emails using the locked format (2-3 lines middle, exactly 1 project mapped, no "I recently applied").

## OPEN THREADS / NEXT STEPS
1. **Run the Drafting Prompt**: Paste the 23-row list and the drafting prompt into the YC agent.
2. **QC the Drafts**: Review the generated `.md` files in `drafts/` against the locked formatting rules.
3. **Manual Send**: User must send the emails manually from Gmail.
4. **Backfill `date_sent`**: Populate the 38 SENT rows in `00-tracking.csv` to trigger Day-5 follow-up logic.

## DO NOT
- Do not attempt to scrape Apollo.io or LinkedIn (proven blocked).
- Do not use Firecrawl, Coldreach, or `mcpman`/`mcpsmgr`.
- Do not write emails longer than 2–3 lines in the middle paragraph.
- Do not include "I recently applied for [role]" or multiple projects in one email.
- Do not invent email addresses or statistics not in the JD.
- Do not send or submit automatically — human approval required.

