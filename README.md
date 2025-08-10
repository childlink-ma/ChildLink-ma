# ChildLink-MA — Medically-Grounded AI Assistant for Neurodiversity (RAG)

**Public beta v0.3 — August 2025**
Migrated to **text-embedding-3-small (1536)**, integrated a new **FAISS v3 (cosine)** index, delivers **multi-source** answers (≤150 words) with final **“References: \[Org, Year]”** line, and removes disclaimer from JSON (displayed in UI).

---

## 🧠 Overview

**ChildLink-MA** is an open-source, multilingual AI assistant designed to provide **medically accurate, concise, and referenced** responses for parents and professionals supporting neurodiverse children (Autism, ADHD, Down Syndrome).
It is built under a **non-profit initiative**, leveraging trusted clinical guidelines while prioritizing **ethical, inclusive AI usage**.

> ⚖️ **Ethical by design**: No internet access. No hallucination. Only validated clinical sources.

---

## 🔍 Key Features

* **Real-time RAG (Retrieval-Augmented Generation)** over vetted clinical guidance (ASD, Down syndrome, ADHD…)
* ≤150-word **multi-source synthesis**, fallback only when corpus is irrelevant
* Clean citations (deduped, “References” label in EN)
* **Medically grounded**: national/international guidelines (NICE, HAS, CDC…)
* **Multilingual answers** (French, Arabic, English…)
* **Rate-limit per IP** (default 3/day; configurable)
* **Built on Azure OpenAI GPT-4.1-mini**
* **FAISS v3 (IndexFlatIP cosine)** indexing
* Optional **WordPress frontend** integration
* **Webhook feedback** (Make.com → Google Sheets)

---

## ⚙️ Architecture

```
PDF Guidelines → Chunking → Embedding (text-embedding-3-small, 1536) → FAISS v3 cosine index
                                                          ↓
                                             GPT-4.1-mini RAG Agent
                                                          ↓
                                         Response + Sources + Disclaimer (UI)
```

---

## 🧱 Tech Stack

| Layer               | Tool / Service                   |
| ------------------- | -------------------------------- |
| LLM                 | GPT-4.1-mini (Azure)             |
| Embeddings          | text-embedding-3-small (1536)    |
| Vector DB           | FAISS v3 (IndexFlatIP cosine)    |
| API Framework       | Flask                            |
| Hosting             | Docker → Azure Web App           |
| Frontend (optional) | WordPress (iframe `widget.html`) |
| Feedback Loop       | Make.com + Google Sheets         |

---

## 🔑 ENV Variables (key)

```
AZURE_OPENAI_API_KEY
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_API_VERSION=2024-10-21
OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4.1-mini
OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
EMBEDDING_DIM=1536
FAISS_INDEX_PATH=/app/clm_index_v3.index
FAISS_METADATA_PATH=/app/clm_metadata_v3.json
FRONTEND_ORIGINS=https://childlink-ma.org,https://www.childlink-ma.org
```

---

## 💡 Use Cases

* Parents seeking **medically validated** answers
* Special educators for early diagnosis/intervention
* Primary care professionals needing quick references

---

## 🚀 Local Run

```bash
python app.py
# Health check:
curl http://localhost:5000/healthz
# Example query:
curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" \
     -d '{"question": "What are early signs of autism?"}'
```

---

## 📦 Build / Deploy

* Docker build/push → Azure Web App
* Include FAISS files in `/app/` for deployment

---

## 📜 License

Released under **Creative Commons BY-NC-SA 4.0** — Free for non-commercial use, with attribution, under the same license.

---

## 🤝 Contributing

Welcoming contributions from:

* Pediatricians, psychologists, neurodevelopment experts
* AI developers focused on ethical use
* Translators and accessibility experts

---

## 📧 Contact / Initiative

Led by **Dr. Fatima Azzahra Mastari** under the **ChildLink-MA** non-profit initiative.

📩 Email: [admin@childlink-ma.org](mailto:admin@childlink-ma.org)
🌐 Website: [childlink-ma.org](https://childlink-ma.org)

---

## 🌍 Let’s build ethical, inclusive AI for good.
