# ChildLink-MA — Medically-Grounded AI Assistant (RAG)

**Public beta v0.3 — August 2025**  
This release migrates to **text-embedding-3-small (1536)**, ships a new **FAISS v3 (cosine)** index, produces **multi-source** answers (≤150 words) with a final **“References: [Org, Year]”** line, and returns **no disclaimer in JSON** (the UI shows it).

## Features
- RAG over vetted clinical guidance (ASD, Down syndrome, ADHD…)
- ≤150-word synthesis, multi-source; fallback only when corpus is not relevant
- Clean citations (deduped, no “NC”); UI label **“References”** in EN
- Multilingual answers (user’s language)
- Rate-limit per IP (default 3/day; configurable)

## Stack
Azure OpenAI GPT-4.1-mini • text-embedding-3-small • FAISS (IndexFlatIP cosine) • Flask • Docker (Azure Web App) • WordPress iframe (`widget.html`)

## ENV (key)
AZURE_OPENAI_API_KEY • AZURE_OPENAI_ENDPOINT • AZURE_OPENAI_API_VERSION=2024-10-21  
OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4.1-mini • OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small • EMBEDDING_DIM=1536  
FAISS_INDEX_PATH=/app/clm_index_v3.index • FAISS_METADATA_PATH=/app/clm_metadata_v3.json  
FRONTEND_ORIGINS=https://childlink-ma.org,https://www.childlink-ma.org

## Local run
`python app.py` → `GET /healthz` → `POST /ask {"question":"..."}`

## Build/Deploy
Docker build/push → Azure Web App. Include FAISS files in `/app/`.
