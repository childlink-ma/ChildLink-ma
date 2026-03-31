# ChildLink-MA — AI Assistant (RAG)

**Public beta v0.4 — April 2026**
Multilingual RAG assistant for families of neurodiverse children (Autism, Down Syndrome, ADHD).
Grounded in clinical guidelines · Zero hallucination · GDPR compliant · Free & open-source.

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Nonprofit](https://img.shields.io/badge/initiative-nonprofit-green)](https://childlink-ma.org)
[![RNA](https://img.shields.io/badge/RNA-W941020510-blue)](https://childlink-ma.org)

---

## Overview

ChildLink-MA Assistant is a **RAG (Retrieval-Augmented Generation)** API that answers questions about neurodevelopmental disorders using vetted clinical sources (NICE, HAS, CDC, AAP, WHO).

> Ethical by design: no internet access, no hallucination, only validated clinical sources.

**Sister repo:** [ChildLink-MA Simulator](https://github.com/childlink-ma/ChildLink-simulator) — behavioral training simulator for parents.

---

## Architecture

```
PDF Guidelines → Chunking → Embedding (text-embedding-3-small, 1536d)
                                        ↓
                               FAISS v3 cosine index
                                        ↓
                             GPT-4.1-mini RAG agent
                                        ↓
                     Response (≤150 words) + References + Citations
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| LLM | GPT-4.1-mini (Azure OpenAI) |
| Embeddings | text-embedding-3-small (1536d) |
| Vector DB | FAISS v3 (IndexFlatIP cosine) |
| Backend | Flask 3.1 + Gunicorn |
| Hosting | Docker → Azure Web App (francecentral) |
| Frontend | `frontend/assistant.html` (standalone) |
| WP integration | `wp-blocks/` (iframe blocks) |
| Feedback loop | Make.com webhook → Google Sheets |

---

## Repo Structure

```
ChildLink-assistant/
├── app.py                        # Flask RAG backend
├── utils.py                      # FAISS load + semantic search
├── rebuild_index_v3.py           # Index rebuild script
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── .env.example                  # ENV vars template (no secrets)
├── frontend/
│   ├── assistant.html            # Standalone frontend (voice + text)
│   └── widget_voice.html         # Split-layout widget (assistant + training)
├── wp-blocks/
│   ├── wp_privacy_block.html     # GDPR privacy block (6 languages)
│   ├── wp_cgu_block.html         # Terms of use block (6 languages)
│   └── wp_guidelines_scroll.html # Clinical guidelines scroll (ASD/T21)
├── data/                         # Clinical guidelines (PDF chunks — not versioned)
├── tests/
│   └── test_ask.py
└── .github/
    └── workflows/
        └── docker-build.yml      # CI: build + push to Docker Hub
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your values. **Never commit `.env`.**

```bash
cp .env.example .env
```

Key variables:

| Variable | Description |
|---|---|
| `AZURE_OPENAI_API_KEY` | Azure OpenAI key |
| `AZURE_OPENAI_ENDPOINT` | Azure endpoint URL |
| `AZURE_OPENAI_API_VERSION` | e.g. `2024-10-21` |
| `OPENAI_CHAT_DEPLOYMENT_NAME` | e.g. `gpt-4.1-mini` |
| `OPENAI_EMBEDDING_DEPLOYMENT` | e.g. `text-embedding-3-small` |
| `EMBEDDING_DIM` | `1536` |
| `FAISS_INDEX_PATH` | `/app/clm_index_v3.index` |
| `FAISS_METADATA_PATH` | `/app/clm_metadata_v3.json` |
| `FRONTEND_ORIGINS` | Comma-separated allowed origins |
| `DAILY_ASK_LIMIT` | Default `3` |
| `MAKE_WEBHOOK_URL` | Optional — feedback webhook |

---

## Local Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables
cp .env.example .env  # then edit .env

# 3. Run
python app.py

# Health check
curl http://localhost:8000/healthz

# Example query
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are early signs of autism?"}'
```

---

## Docker

```bash
# Build
docker build -t childlinkma/childlinkma:latest .

# Run
docker run -p 8000:8000 --env-file .env childlinkma/childlinkma:latest
```

---

## Rebuild FAISS Index

After adding new PDF guidelines to `data/`:

```bash
python rebuild_index_v3.py
```

This regenerates `clm_index_v3.index` and `clm_metadata_v3.json`.

---

## API Reference

### `POST /ask`

```json
{
  "question": "How do I manage a meltdown?",
  "history": [],
  "top_k": 6
}
```

Response:
```json
{
  "answer": "...",
  "citations": [{"source": "NICE NG11", "year": "2021"}]
}
```

Rate limit: 3 requests/day/IP (configurable via `DAILY_ASK_LIMIT`).

### `POST /feedback`

```json
{"signal": "up"}
```

### `GET /healthz`

Returns service status, FAISS state, model info.

---

## WordPress Integration

Drop any file from `wp-blocks/` into a WordPress **Custom HTML** block.
Each block auto-detects browser language (EN/FR/AR/ES/PT/SW).

---

## Performance (v0.4)

| Metric | Value |
|---|---|
| Accuracy (RAG) | 92% |
| Hallucination rate | 0% |
| Avg latency | 1.4s |
| Multilingual queries tested | 120 |
| Languages | EN · FR · AR · ES · PT · SW |

---

## License

[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) — Free for non-commercial use, with attribution, same license.

---

## Nonprofit

Led by **Dr. Fatima Azzahra Mastari** under the **ChildLink-MA** nonprofit.
RNA W941020510 · SIRET 989 176 201 00014 · Vitry-sur-Seine, France.

📩 admin@childlink-ma.org · 🌐 childlink-ma.org
