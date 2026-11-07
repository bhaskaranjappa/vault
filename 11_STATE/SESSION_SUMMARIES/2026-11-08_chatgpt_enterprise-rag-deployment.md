# VAULT SESSION SUMMARY — Enterprise RAG Cloud Deployment

## CONTEXT
Enterprise RAG cloud deployment, Zilliz Cloud database migration, Groq model replacement, Hugging Face deployment, and public-demo security review. The project moved from a broken Hugging Face deployment to an owner-confirmed working RAG application. Core database connectivity, collection creation, document ingestion, retrieval configuration and Qwen generation were addressed. Public data/secret exposure remains unresolved.

## STACK / ENVIRONMENT
- Windows 11; PowerShell 7.6.x.
- Local project: `C:\Users\ABhas\projects\enterprise-rag`.
- Python 3.14 user installation for Hub commands; `huggingface_hub==1.21.0` restored after an incompatible upgrade to 2.4.0.
- GitHub: `bhaskaranjappa/Enterprise-RAG`, branch `main`.
- Hugging Face Space: `BhaskarAnjappa/Enterprise_RAG`; live URL: https://bhaskaranjappa-enterprise-rag.hf.space.
- Latest GitHub HEAD observed: `b0c2b73b3b1c62a22b7a9bb2519942fac3b822c1`.
- Stack: Streamlit, FastAPI/Uvicorn, PyMilvus, Zilliz Cloud Serverless, BAAI/bge-small-en-v1.5, BM25, Reciprocal Rank Fusion, CrossEncoder reranking, Groq API, Qwen 3.8 27B.
- Zilliz: cluster `Free-01`, AWS Frankfurt (`aws-eu-central-1`), collection `knowledge_base`, 384-dimensional float vector, COSINE AUTOINDEX.
- Secrets are not reproduced in this summary.

## WHAT'S BEEN DONE

### 1. Selective deployment workflow
Bhaskar challenged the need for complete GitHub-to-Hugging-Face synchronization. Decision: selective file deployment is the default. Do not mirror the complete Git tree automatically; this could delete Space-specific files and runtime data.

Local Git commands successfully updated the project from GitHub:
```powershell
git fetch origin
git pull --ff-only origin main
```

### 2. Zilliz connection and endpoint correction
The original Space error referenced a GCP West US hostname:
```
MilvusException: Fail connecting to server on
in03-e6d74f9a99c64f0.serverless.gcp-us-west1.cloud.zilliz.com:443
```
The cluster was running. Bhaskar opened the actual cluster `Free-01` in AWS Frankfurt and copied the Public Endpoint from the Connect panel. The replacement endpoint and Zilliz token were configured in Hugging Face Space settings. The local migration subsequently connected successfully.

Required configuration:
- `ZILLIZ_ENDPOINT`: public serving endpoint, not the Zilliz console management URL.
- `ZILLIZ_TOKEN`: valid API key/token.
The endpoint and token are separate settings.

### 3. Collection naming / schema / retrieval
The original application expected `upsc_knowledge_base`, but the new cluster had no collections. Bhaskar selected `knowledge_base`.

GitHub changes:
- `retrieval/hybrid_search.py`: renamed collection; Zilliz AUTOINDEX uses `level: 1`; local IVF_FLAT fallback retains `nprobe: 10`.
- `ingestion/migrate_to_cloud.py`: creates `knowledge_base`, 384-dimensional embedding schema, COSINE AUTOINDEX, checks for PDFs and prevents duplicate insertion into a non-empty collection.
- `ingestion/embed_store.py`: local collection renamed.
- `README.md`: collection documentation aligned.

### 4. Cloud ingestion succeeded
Bhaskar ran:
```powershell
python ingestion\migrate_to_cloud.py
```
The local `data/` directory contained 10 PDFs. The script reported schema/index creation, generated BGE-small embeddings, inserted vectors and flushed the collection. Final output: `Cloud migration completed successfully.`

Reported vector insertions:
| Document | Vectors |
|---|---:|
| World History | 479 |
| Environment & Ecology | 1,187 |
| Ethics | 1,203 |
| Geography & Disaster Management | 1,360 |
| Governance | 701 |
| Indian Society | 1,017 |
| Internal Security | 1,145 |
| Modern India | 969 |
| Post Independence India | 471 |
| Social Justice | 1,042 |
| **Total** | **9,574** |

This is the migration terminal's reported insert count, not a separate independent database count. Do not rerun migration casually; the script refuses to insert into a non-empty collection.

### 5. Retrieval code deployed to Hugging Face
A direct ChatGPT-side Hugging Face Jobs deployment attempt returned `402 Payment Required`. Bhaskar authenticated locally with:
```powershell
hf auth login
```
Browser OAuth login succeeded. He then uploaded only `retrieval/hybrid_search.py` using `HfApi.upload_file`.

Space commit:
`44c81456aed10fc4dcf6543e9428a31eecb95db2`

The deployed file was read back and verified:
- Collection name is `knowledge_base`.
- Old `upsc_knowledge_base` reference is absent.
- Zilliz Cloud parameter `level: 1` is present.
- Local fallback `nprobe: 10` remains.

### 6. Startup and Groq failures
Subsequent Space logs showed:
- Uvicorn/Streamlit running on port 7860.
- No Milvus connection or missing-collection error.
- BGE embedding weights loaded (199/199).

Then Groq returned:
- First: `401 invalid_api_key`. Bhaskar generated a new Groq key and updated Space settings.
- Second: `404 model_not_found` for `llama-3.3-70b-versatile`.

### 7. Qwen 3.8 27B replacement
Bhaskar requested Qwen 3.8 27B. Exact Groq model ID used:
`qwen/qwen3.8-27b`.

GitHub `api/generate.py` now sets:
```python
GROQ_MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")
GROQ_REASONING_EFFORT = "none"
```
Both query decomposition and final answer calls use the Qwen model with instruct-mode sampling:
- `temperature=0.7`
- `top_p=0.8`
- `reasoning_effort="none"`
- `reasoning_format="hidden"`

Also updated `.env.example` and README to document Qwen and remove the obsolete Llama model reference. Hugging Face's deployed `api/generate.py` was inspected and contained Qwen configuration. Bhaskar subsequently confirmed: **"it is working."** This is owner-confirmed functionality; no formal evaluation suite was run.

### 8. Hugging Face Hub anonymous warning
Space logs included:
`Warning: You are sending unauthenticated requests to the HF Hub.`
A read-scoped token stored as Space Secret `HF_TOKEN` was recommended. Completion is unverified. The embedding model download succeeded without authentication.

### 9. Public demo / visitor exposure
The public Space URL and direct app link were discussed. The Streamlit message about usage statistics is telemetry, not an app shutdown warning. Optional configuration:
```toml
[browser]
gatherUsageStats = false
```
No telemetry change was confirmed.

Direct inspection of the Space repository showed:
- Root contains `.env` (335 bytes at inspection), plus `data/`, `volumes/`, application source and other files.
- All 10 source PDFs remain in public `data/`.
- Earlier inspection found populated Groq and Zilliz credentials in the public `.env`; values were not copied into this record.
- The deployed `ui.py` displays retrieved chunk text inside citation expanders, together with source names and page numbers.
Therefore visitors can query the public RAG app and read returned passages; the original PDFs are also independently accessible through the public repository.

Bhaskar was asked whether he wants visitors to see retrieved passages or only answers. No decision yet.

## CURRENT STATE / PROBLEM

### VERIFIED
- GitHub Enterprise RAG main HEAD observed at `b0c2b73b3b1c62a22b7a9bb2519942fac3b822c1`.
- Zilliz migration command completed and reported 9,574 inserted vectors.
- Hugging Face retrieval file deployed and read-back verified.
- Space startup logs showed successful collection/model loading.
- Qwen generation code deployed/inspected.
- Bhaskar confirmed application working after Qwen switch.
- Public Space root still contains `.env` and `data/`; all 10 PDFs were listed.
- Deployed UI exposes full retrieved passages.

### CLAIMED
- Bhaskar rotated old Zilliz credentials and updated Space secrets.
- Bhaskar rotated Groq API key and updated Space secret.
- Bhaskar confirmed the app is working.

### UNKNOWN
- Whether all previously exposed credentials have been fully revoked.
- Whether read-scoped `HF_TOKEN` was added to Space Secrets.
- Whether PDFs may legally/contractually be publicly redistributed.
- Whether passage disclosure or answer-only behaviour is desired.
- Formal retrieval, faithfulness, citation, NOT FOUND and latency metrics.

### BLOCKED / UNRESOLVED
No current core deployment blocker reported. Public secret/source-data exposure and intended visitor access policy remain unresolved.

## KEY DECISIONS + WHY
1. Selective deployment instead of full Space tree synchronization; owner wants control and full sync risks deleting Space-specific data.
2. New collection named `knowledge_base`; use consistently across ingestion and retrieval.
3. Zilliz AUTOINDEX uses `level: 1`; keep local Milvus `nprobe: 10` fallback.
4. Groq uses `qwen/qwen3.8-27b`; prior Llama model returned 404.
5. Keep API keys and tokens in Hugging Face Space Secrets.
6. Do not recreate or blindly repopulate the existing 9,574-vector collection.

## TOOL / RUNTIME USAGE
- ChatGPT GPT-6: code/repository review, diagnosis, GitHub updates, deployment guidance, Hugging Face file inspection.
- GitHub connector: updated Enterprise RAG source files and verified main branch contents.
- Hugging Face filesystem connector: inspected deployed source files and public Space tree.
- Hugging Face Jobs: attempted remote upload; blocked by 402 Payment Required.
- PowerShell: Bhaskar executed Git, migration, Hugging Face authentication and upload.
- Hugging Face Hub Python SDK: successfully deployed selected retrieval file.
- Zilliz Cloud: migration succeeded.
- Groq: model/API authentication errors resolved by owner configuration and Qwen model replacement.
- No ZCode, OpenCode, Antigravity or Freebuff executor used.

## BHASKAR CONTEXT RELEVANT TO THIS SESSION
Bhaskar explicitly prefers selective, controlled deployment of individual files to Hugging Face rather than complete tree synchronization.

## OPEN THREADS / NEXT STEPS
1. **First incomplete action — critical:** remove public `.env` from the latest Space revision; confirm all formerly exposed Groq/Zilliz credentials are revoked. Git history may still retain the prior file.
2. Determine whether the 10 PDFs may be publicly redistributed. Remove them from the public Space if not.
3. Decide if visitors can see complete retrieved text or only final answers. If answer-only is desired, change `ui.py` to remove citation expanders exposing the full passages.
4. Add read-scoped `HF_TOKEN` Space Secret if desired; verify after.
5. Verify local Git working copy is at latest main.
6. Run formal RAG evaluation: retrieval relevance, answer faithfulness, citation correctness, NOT FOUND handling and latency breakdown.
7. Continue without repeating completed Zilliz migration.

## DO NOT
- Do not full-sync the Space tree by default.
- Do not rerun cloud migration against the populated collection.
- Do not drop/recreate `knowledge_base`.
- Do not restore `upsc_knowledge_base`.
- Do not revert to the old Llama model.
- Do not put credentials in endpoint fields or public files.
- Do not claim public exposure is resolved merely because credentials were rotated.

## CANONICAL WRITE-BACK CANDIDATES
- `08_KNOWLEDGE/PROJECTS/ENTERPRISE_RAG_KNOWLEDGE_BASE.md`: expanded project/runtime/deployment/security state.
- `11_STATE/STATE_INDEX.md`: current Enterprise RAG state and blockers.
- `07_VERSION_TRACKING/DECISION_HISTORY.md`: deployment, collection, model and no-reingestion decisions.
- This full summary: `11_STATE/SESSION_SUMMARIES/2026-11-08_chatgpt_enterprise-rag-deployment.md`.

## PROVENANCE / CONFIDENCE
- User terminal output: Git pulls, PDF inventory, migration output/vector counts, HF OAuth login, successful upload commit.
- Repository inspection: source files, model config, commits and branch contents.
- Hugging Face filesystem inspection: deployed files, root entries, public PDFs, `.env` existence and citation display code.
- User statement: app works after Qwen replacement.
- Inference: public Space files and UI enable direct PDF and passage access, supported by direct repository/code inspection.
- Unverified: actual database entity count outside migration output; formal answer quality/latency; current historical credential revocation status.

## SESSION METADATA
- Session date: 2026-11-07 to 2026-11-08
- Session timezone: Asia/Kolkata (IST, UTC+05:30)
- Approximate start time: unknown; earliest available reference approximately 2026-11-07 22:49 IST.
- End time: unknown.
- Closeout generated at: 2026-11-08; exact time unknown.
- AI runtime: ChatGPT GPT-6.
- Coding executor: none; Bhaskar ran local PowerShell commands.
- Project/repository: `bhaskaranjappa/Enterprise-RAG`; deployment `BhaskarAnjappa/Enterprise_RAG`; continuity repository `bhaskaranjappa/vault`.
- Primary task: restore and verify Enterprise RAG deployment, migrate vectors to Zilliz Cloud, and replace Groq generation model.
- Status at close: core application owner-confirmed working; public `.env` and source PDF exposure unresolved.
