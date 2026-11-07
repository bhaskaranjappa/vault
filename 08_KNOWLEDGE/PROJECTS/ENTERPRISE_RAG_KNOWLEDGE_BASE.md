# ENTERPRISE RAG & KNOWLEDGE BASE

Status: **LIVE / OWNER-CONFIRMED WORKING** (2026-11-08). Formal quality and latency benchmarks remain unrun.

## Repository and deployment

- GitHub source: [bhaskaranjappa/Enterprise-RAG](https://github.com/bhaskaranjappa/Enterprise-RAG), branch `main`.
- Hugging Face Space: [BhaskarAnjappa/Enterprise_RAG](https://huggingface.co/spaces/BhaskarAnjappa/Enterprise_RAG).
- Direct demo: https://bhaskaranjappa-enterprise-rag.hf.space
- Local Windows project: `C:\Users\ABhas\projects\enterprise-rag`.
- Deployment policy: **selective file deployment** from GitHub/local working tree to Hugging Face. Do not mirror the entire Git tree by default; full-tree sync could delete Space-specific files and data.
- GitHub HEAD observed during the 2026-11-07/08 session: `b0c2b73b3b1c62a22b7a9bb2519942fac3b822c1` (Qwen README update).

## Architecture / stack

Streamlit UI and FastAPI API; PDF extraction/chunking; BAAI/bge-small-en-v1.5 embeddings; Zilliz Cloud (PyMilvus); dense vector search; BM25 keyword retrieval; Reciprocal Rank Fusion; CrossEncoder reranking; Groq-hosted Qwen generation.

### Cloud vector database

- Zilliz cluster: `Free-01`, AWS Frankfurt (`aws-eu-central-1`).
- Collection: `knowledge_base`.
- Schema: auto-ID INT64 primary key; `source` VARCHAR; `page` INT64; `text` VARCHAR; `embedding` FLOAT_VECTOR with dimension 384.
- Index: COSINE / AUTOINDEX.
- Retrieval config: Zilliz Cloud uses `level: 1`; local Milvus IVF_FLAT fallback retains `nprobe: 10`.
- Connection settings are separate Space Secrets/Variables: `ZILLIZ_ENDPOINT` (public serving endpoint) and `ZILLIZ_TOKEN` (API key or valid cluster credential token). Never put the console management URL in the endpoint.

### Ingestion

On 2026-11-07/08, Bhaskar ran `python ingestion\migrate_to_cloud.py` locally against the new Zilliz cluster. The terminal reported successful schema/index creation, upload and flush for 10 PDFs.

Reported inserted vectors by source:
- World History: 479
- Environment & Ecology: 1,187
- Ethics: 1,203
- Geography & Disaster Management: 1,360
- Governance: 701
- Indian Society: 1,017
- Internal Security: 1,145
- Modern India: 969
- Post Independence India: 471
- Social Justice: 1,042
- **Total reported inserted: 9,574 vectors.**

This is migration command output, not a separate post-migration database count or quality benchmark. Do not rerun migration casually: the current script stops when the target collection already contains entities, preventing accidental duplicate insertion.

### Generation

- Provider: Groq.
- Model: `qwen/qwen3.8-27b`.
- GitHub `api/generate.py` defaults to `GROQ_MODEL=qwen/qwen3.8-27b`, with environment override.
- Both query decomposition and answer-generation calls use the configured model with instruct-mode settings (`reasoning_effort="none"`, hidden reasoning format).
- `GROQ_API_KEY` is a Space Secret. `GROQ_MODEL` can be configured as a Space Variable, but code has the Qwen default.
- The earlier `llama-3.3-70b-versatile` model returned model-not-found and was replaced.

## Current application behaviour

- Hugging Face Docker Space starts Streamlit on port 7860.
- The deployed retrieval file was selectively uploaded and read back successfully. Commit: `44c81456aed10fc4dcf6543e9428a31eecb95db2`.
- Direct read-back verified `knowledge_base`, Zilliz `level: 1`, and local `nprobe: 10` fallback.
- Startup logs subsequently showed Streamlit/Uvicorn start, no Milvus connection/collection exception, and successful loading of 199 embedding-model weights.
- Groq first returned 401 for an invalid key, then the old Llama model returned 404. Bhaskar replaced credentials/model configuration and later confirmed: **"it is working."**
- Owner-confirmed working after Qwen switch. No formal benchmark was run for retrieval relevance, faithfulness, citation accuracy, NOT FOUND behaviour, or latency.
- BM25 requires a local PDF corpus in the Space; absent PDFs, dense retrieval can still run, but hybrid keyword retrieval is unavailable. The deployed Space still contained the `data/` folder during the security inspection.

## Security and public-demo state — unresolved

Direct inspection of the public Space repository during the 2026-11-08 session showed:
- Root contains a tracked `.env` file (335 bytes at inspection). An earlier inspection found populated Groq and Zilliz credentials in that public file. Values are intentionally not recorded here.
- All 10 source PDFs are still present under public `data/`.
- The deployed `ui.py` expands citations and displays retrieved passage text alongside source filenames and page numbers.
- Visitors can query the public RAG application and retrieve passages. The original PDFs are also directly accessible through the public Space repository.
- Replacement Groq and Zilliz credentials were reported by Bhaskar as configured. Rotation does **not** erase historical exposure. Verify every formerly exposed key is revoked and remove `.env` from the latest Space revision; historical Git exposure still needs separate consideration.
- Authorization to redistribute the 10 source PDFs has not been established. Remove them from the public Space if redistribution is not permitted.
- Visitor policy remains undecided: display retrieved passages, or show answer text only. This must be an explicit product/security decision.
- A read-scoped `HF_TOKEN` Space Secret was recommended to reduce anonymous Hub download/rate-limit exposure; completion is unverified.

## Decisions and operating constraints

1. Selective Hugging Face file deployment is the default; do not perform full-tree synchronization without an explicit need.
2. Keep the Zilliz collection name `knowledge_base` consistent across retrieval and ingestion.
3. Use Zilliz AUTOINDEX search parameter `level: 1`; retain local `nprobe: 10` fallback.
4. Use Groq Qwen 3.8 27B (`qwen/qwen3.8-27b`) instead of the unavailable Llama model.
5. Keep Groq, Zilliz and Hugging Face credentials in Space Secrets; never commit actual credentials.
6. Do not recreate/drop or blindly re-ingest the populated cloud collection.

## Next work

1. Critical: remove the public Space `.env` and verify all previously exposed credentials are revoked.
2. Confirm whether source PDFs may be publicly redistributed; remove from the public Space if not.
3. Decide whether visitors may see full retrieved passages or answers only; update `ui.py` accordingly.
4. Consider read-scoped `HF_TOKEN` Space Secret; currently unverified.
5. Run a proper RAG evaluation: retrieval relevance, faithfulness, citation correctness, NOT FOUND handling, and latency breakdown.

Numeric quality/performance claims remain **CLAIMED** unless independently validated.
