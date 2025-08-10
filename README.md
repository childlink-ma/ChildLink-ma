# 🧠 ChildLink-MA: Medically-Grounded AI Assistant for Neurodiversity

**ChildLink-MA** is a multilingual, ethical, open-source AI assistant designed to provide medically accurate, concise, and referenced answers to parents and professionals supporting neurodivergent children (autism, Down syndrome).

This project is led by the nonprofit association **ChildLink-MA**, registered in France (RNA: W751267470 / SIRET: 91815431900017).

**Status:** Public Beta – v0.2 – July 2025

---

## 🎯 Objectives

* Provide **free and reliable access** to clinical recommendations from validated medical sources.
* Reduce the **information gap** for isolated families and professionals.
* Promote **inclusive and ethical AI**, free of hallucinations, ads, or tracking.

---

## ⚙️ Key Features

* ✅ Real-time **RAG (Retrieval-Augmented Generation)**
* ✅ Answers capped at **150 words max**, with mandatory **citations** in `[Organization, Year]` format
* ✅ Secondary GPT generation only **if no relevant document info is found** (100 words max)
* ✅ **Multilingual**: FR, EN, AR... with automatic language detection
* ✅ Medical **disclaimer translated** into the detected language
* ✅ AI deployable **locally or via Azure**, with no internet access required

---

## 🧱 Technology Stack

| Component           | Technology Used                           |
| ------------------- | ----------------------------------------- |
| LLM                 | Azure OpenAI GPT-4.1-mini                 |
| Embeddings          | text-embedding-ada-002                    |
| Vector store (dev)  | FAISS (local, RAG-optimized)              |
| Vector store (prod) | Azure Cognitive Search                    |
| Backend API         | Python (Flask)                            |
| User frontend       | WordPress.org (HTML form + custom JS)     |
| Document storage    | Azure Blob Storage                        |
| Feedback tracking   | Webhook to Google Sheets (Make, optional) |
| Deployment (prod)   | Azure Web App or local server             |

---

## 🧠 AI Prompt (Strictly Enforced)

> The agent is a medical assistant specializing in neurodevelopmental disorders (autism, Down syndrome, ADHD, etc.).
> It must use **only the provided documents**.
> Responses must be **150 words max**, with mandatory **citations** in `[Organization, Year]` format.
> If no relevant source is found, say so, then generate a GPT-based response (max 100 words), clearly labeled.
> Always reply in the **language of the question**.
>
> **Mandatory disclaimer (automatically translated):**
> *"This content is provided for informational purposes only and does not replace a consultation with a qualified healthcare professional. This assistant is a support tool and not a medical device."*

---

## 📂 Project Structure

```text
childlink-ma/
├── README.md                 # Project overview
├── LICENSE                   # License (CC BY-NC-SA 4.0)
├── .gitignore                # Files to exclude (env, cache, etc.)

├── data/                     # Source medical documents (PDFs, text)
│   └── ...                   # Parsed guideline files

├── scripts/                  # Python processing & querying scripts
│   ├── parse_pdf.py          # PDF text extraction
│   ├── chunking.py           # Chunking into clean segments
│   └── query_index.py        # RAG querying with dynamic prompt + fallback

├── prompt/                   # Multilingual prompt logic
│   └── base_prompt.txt       # Full prompt with ethical rules

├── app/                      # Flask backend (REST API)
│   ├── app.py                # Main server file
│   ├── routes.py             # Query processing logic
│   └── utils.py              # Helper functions / loading / preprocessing

├── frontend/                 # WordPress integration (HTML + JS)
│   ├── form.html             # Simple frontend form
│   └── submit.js             # API call to backend

├── docs/                     # Internal & external documentation
│   ├── architecture.png      # RAG schema (coming soon)
│   └── specs.md              # Technical notes & specs
```

---

## 📌 Use Cases

* 👩‍👦 Parents seeking reliable answers on neurodevelopmental conditions
* 👩‍⚕️ Professionals (educators, caregivers, clinicians) needing structured guidance
* 🧑‍💻 Developers and researchers working on healthcare-related RAG

---

## 🛠️ Next Steps

### 🔧 Technical Phase

* ✅ Implemented local processing pipeline: `parse_pdf.py → chunking.py → FAISS index`
* ✅ Integrated dynamic multilingual prompt logic in `query_index.py`
* ✅ Applied strict formatting constraints: 150 words max + `[Organization, Year]` citation
* ✅ Implemented GPT fallback logic when no vector match is found
* ✅ Integrated language auto-detection and disclaimer translation logic
* ✅ Structured backend API with Flask (`app.py`, `routes.py`, `utils.py`)
* ✅ Connected local FAISS-based RAG to production-ready API endpoint
* ⏳ Preparing CLI tool for batch testing and document vectorization
* ⏳ Planning API rate limiting and logging for local + Azure versions

### 🌐 Deployment & Outreach

* ⏳ Publish the GitHub repository under a public license (done locally)
* ⏳ Publish an article on Medium and OpenWHO (in progress)
* ⏳ Prepare institutional and personal LinkedIn posts (Q3 2025)
* ⏳ Record and release a short demo video (GIF or clip format)

### 🧪 QA & User Feedback

* ⏳ Run expert review on a sample of 50 AI responses (manual validation)
* ⏳ Set up a feedback collection form integrated with Google Sheets
* ⏳ Track fallback triggers and "no source found" events for monitoring

### 🌍 Internationalization & Accessibility

* ✅ Arabic and English versions of parsing and prompts planned
* ⏳ Prepare multilingual interface (FR, EN, AR – scalable to 6 UN languages)
* ⏳ Improve accessibility: mobile-first design, voice-ready outputs

### ⚖️ Compliance & Ethics

* ⏳ Draft CNIL notice and logging policy (depending on deployment model)
* ⏳ Finalize GDPR documentation and data handling policies
* ⏳ Write and publish the ethical AI manifesto for the health domain

---

## 🤝 Contributing

The project is currently in **public beta**. Contributions are welcome in:

* Curating medical open-access documents
* Improving scripts (Python, Flask, JS)
* Translating to FR/EN/AR

**Contact:** [admin@childink-ma.org](mailto:admin@childink-ma.org)
**Connect with the founder:** [LinkedIn – Dr Mastari](https://www.linkedin.com/in/drmastari/)

---

## 🔗 Learn More

For more information about the broader ChildLink-MA initiative, visit the institutional website:

👉 [www.childlink-ma.org](https://www.childlink-ma.org)

---

## 📜 License

**Creative Commons BY-NC-SA 4.0 International**

You are free to **share and adapt** this project under the following terms:

* Attribution required (**BY**)
* Non-commercial use only (**NC**)
* Share alike (**SA**) under the same license
