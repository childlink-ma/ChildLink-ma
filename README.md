# ChildLink-MA: Medically-Grounded AI Assistant for Neurodiversity

## 🧠 Overview
**ChildLink-MA** is an open-source, multilingual AI assistant designed to provide medically accurate, concise, and referenced responses for parents and professionals supporting neurodiverse children (Autism, ADHD, Down Syndrome). Built as part of a non-profit initiative, the assistant leverages trusted clinical guidelines and prioritizes ethical, inclusive AI usage.

> ⚖️ **Ethical by design**: No internet access. No hallucination. Only validated clinical sources.

---

## 🔍 Key Features
- **Real-time RAG (Retrieval-Augmented Generation)**
- **Medically grounded**: sources from national/international guidelines (e.g., NICE, HAS, CDC)
- **Multilingual**: supports French, Arabic, English, etc.
- **Built on Azure OpenAI (GPT-4.1-mini)**
- **Embeddings via `text-embedding-ada-002`**
- **Azure Cognitive Search indexing**
- **WordPress frontend integration** (optional)
- **Webhook for feedback (Make.com > Google Sheets)**

---

## ⚙️ Architecture

1. **PDF Guidelines** (validated clinical documents)  
2. → **Chunking & Embedding** via `text-embedding-ada-002`  
3. → Stored in **Azure Cognitive Search**  
4. → Queried by **GPT-4.1-mini** (via RAG)  
5. → Generates **concise, cited response + sources + disclaimer**

---

## 💡 Use Cases
- Parents looking for medically validated answers
- Special educators supporting early diagnosis/intervention
- Primary care professionals accessing quick references

---

## 🧱 Tech Stack
| Layer               | Tool / Service             |
|--------------------|----------------------------|
| LLM                | GPT-4.1-mini (Azure)       |
| Embeddings         | `text-embedding-ada-002`   |
| Vector DB          | Azure Cognitive Search     |
| File Storage       | Azure Blob Storage         |
| Frontend (optional)| WordPress site             |
| Feedback Loop      | Make.com + Google Sheets   |

---

## 🚀 Setup (coming soon)
- Python scripts for parsing/chunking
- Azure setup templates (Cognitive Search, AI services)
- `.env.template` for environment variables
- Optional WordPress integration steps

---

## 📜 License
This project is released under **Creative Commons BY-NC-SA 4.0** — You are free to reuse it non-commercially, with attribution, and under the same license.

---

## 🤝 Contributing
Open to contributions from:
- Pediatricians, psychologists, neurodevelopment experts
- AI developers focused on ethical use
- Translators and accessibility experts

---

## 📧 Contact / Initiative
This project is led by Dr. Fatima Azzahra Mastari as part of the **ChildLink-MA** non-profit initiative.

📩 Email: [admin@childlink-ma.org](mailto:admin@childlink-ma.org)  
🌐 Website: [childlink-ma.org](https://childlink-ma.org)

---

## 🌍 Let’s build ethical, inclusive AI for good.


---

## 🌍 Let’s build ethical, inclusive AI for good.
