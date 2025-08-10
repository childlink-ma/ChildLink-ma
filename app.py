import os
import time
import hashlib
import re
import json
import datetime
from collections import defaultdict

from flask import Flask, request, jsonify, send_file, make_response, redirect
from flask_cors import CORS
from openai import AzureOpenAI
import httpx
from langdetect import detect  # facultatif
from utils import load_faiss, semantic_search

# ========= Configuration =========
AZURE_OPENAI_API_KEY      = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_ENDPOINT     = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_VERSION  = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")

OPENAI_EMBEDDING_DEPLOYMENT = os.getenv("OPENAI_EMBEDDING_DEPLOYMENT", "")
OPENAI_CHAT_DEPLOYMENT_NAME = os.getenv("OPENAI_CHAT_DEPLOYMENT_NAME", "")

FAISS_INDEX_PATH    = os.getenv("FAISS_INDEX_PATH", "./clm_index.index")
FAISS_METADATA_PATH = os.getenv("FAISS_METADATA_PATH", "./clm_metadata.json")

PUBLIC_API_KEY   = os.getenv("PUBLIC_API_KEY", "")
FRONTEND_ORIGINS = os.getenv("FRONTEND_ORIGINS", "https://childlink-ma.org,https://www.childlink-ma.org")

# Make (webhook)
MAKE_WEBHOOK_URL    = os.getenv("MAKE_WEBHOOK_URL", "")
MAKE_WEBHOOK_KEY    = os.getenv("MAKE_WEBHOOK_KEY", "")
MAKE_WEBHOOK_HEADER = os.getenv("MAKE_WEBHOOK_HEADER", "x-make-apikey")

# Rate-limit (par défaut 3/jour/IP hachée)
DAILY_ASK_LIMIT = int(os.getenv("DAILY_ASK_LIMIT", "3"))

SYSTEM_PROMPT = (
    "You are a medical assistant focused on neurodevelopmental disorders (Autism, Down Syndrome, ADHD, etc.).\n"
    "STRICT RULES:\n"
    "- Use ONLY the provided documents. If nothing relevant, say so, then provide a clearly marked GPT-generated fallback (max 100 words). "
    "When you use the fallback, prefix the answer with [FALLBACK].\n"
    "- Never diagnose. Encourage consulting qualified professionals. Provide red flags and orientation steps when appropriate.\n"
    "- Max 150 words for the main answer.\n"
    "- Cite sources inline at the end as: Références: [Org, Année]; [Org2, Année2]. Do NOT use numeric citations like [1], [2].\n"
    "- Respond in the user's language.\n"
    "- Do NOT include any disclaimer text in your answer; the UI displays it separately.\n"
)

# ========= App =========
app = Flask(__name__)
allowed = [o.strip() for o in FRONTEND_ORIGINS.split(",") if o.strip()]
CORS(app, resources={
    r"/ask": {"origins": allowed},
    r"/feedback": {"origins": allowed},
    r"/widget.html": {"origins": allowed},
})

# Pare-feu de sortie JSON : pas de disclaimer, citations propres (sans NC)
@app.after_request
def sanitize_response(resp):
    try:
        if resp.mimetype == "application/json":
            payload = json.loads(resp.get_data(as_text=True))

            # 1) supprimer tout 'disclaimer'
            payload.pop("disclaimer", None)

            # 2) nettoyer/dédoublonner les citations (supprimer NC, year optionnelle)
            clean, seen = [], set()
            for c in (payload.get("citations") or []):
                src = (c.get("source") or c.get("org") or "").strip()
                yr  = (c.get("year") or "").strip()
                if not src or src == "NC":
                    continue
                key = (src, yr if yr and yr != "NC" else "")
                if key in seen:
                    continue
                seen.add(key)
                item = {"source": src}
                if key[1]:
                    item["year"] = key[1]
                clean.append(item)
            if "citations" in payload:
                payload["citations"] = clean

            resp.set_data(json.dumps(payload, ensure_ascii=False))
    except Exception:
        pass
    return resp

# ========= Auth =========
@app.before_request
def require_api_key():
    if request.path not in ("/ask", "/feedback"):
        return
    origin  = request.headers.get("Origin", "")
    referer = request.headers.get("Referer", "")
    base    = request.host_url.rstrip("/")
    if (not origin) or origin.startswith(base) or (referer and referer.startswith(base)):
        return
    if PUBLIC_API_KEY and request.headers.get("X-API-Key") != PUBLIC_API_KEY:
        return jsonify({"error": "Non autorisé. Clé API invalide ou absente."}), 401

# ========= Azure OpenAI Client =========
def make_client():
    proxy = os.getenv("HTTPS_PROXY") or os.getenv("HTTP_PROXY")
    http_client = httpx.Client(proxies=proxy, timeout=30) if proxy else httpx.Client(timeout=30)
    return AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version=AZURE_OPENAI_API_VERSION,
        http_client=http_client
    )
client = make_client()

# ========= Data =========
index, metadata = load_faiss(FAISS_INDEX_PATH, FAISS_METADATA_PATH)

SEEN_IPS       = set()
TOTAL_REQUESTS = 0
FALLBACK_COUNT = 0
QUESTIONS_COUNT = defaultdict(int)  # (ip_hash, date_str_utc) -> compteur

# ========= Helpers =========
def ip_hash():
    ip = request.headers.get("X-Forwarded-For", "").split(",")[0].strip() or (request.remote_addr or "")
    return hashlib.sha256(ip.encode()).hexdigest()[:12]

def utc_date_str():
    return datetime.datetime.utcnow().date().isoformat()

def get_country():
    cf_country = request.headers.get("CF-IPCountry")
    return cf_country if cf_country else "Unknown"

def mark_counts(is_fallback: bool):
    global TOTAL_REQUESTS, FALLBACK_COUNT
    TOTAL_REQUESTS += 1
    if is_fallback:
        FALLBACK_COUNT += 1
    SEEN_IPS.add(ip_hash())

def can_ask_today(ip_h: str) -> bool:
    today = utc_date_str()
    key = (ip_h, today)
    if QUESTIONS_COUNT[key] >= DAILY_ASK_LIMIT:
        return False
    QUESTIONS_COUNT[key] += 1
    return True

def send_make(payload: dict):
    if not MAKE_WEBHOOK_URL:
        return
    try:
        headers = {"Content-Type": "application/json"}
        if MAKE_WEBHOOK_KEY:
            headers[MAKE_WEBHOOK_HEADER] = MAKE_WEBHOOK_KEY
        httpx.post(MAKE_WEBHOOK_URL, json=payload, headers=headers, timeout=10)
    except Exception:
        pass

def is_gpt_fallback(contexts, answer: str) -> bool:
    if answer and "[FALLBACK]" in answer.upper():
        return True
    total_ctx = sum(len((c.get("text") or "")) for c in contexts)
    return total_ctx < 40

def build_citations(contexts, max_items=5):
    """Dédoublonne et supprime NC. Conserve year uniquement si renseignée."""
    clean, seen = [], set()
    for c in contexts:
        src = (c.get("source") or c.get("org") or "").strip()
        yr  = (c.get("year") or "").strip()
        if not src or src == "NC":
            continue
        key = (src, yr if yr and yr != "NC" else "")
        if key in seen:
            continue
        seen.add(key)
        item = {"source": src}
        if key[1]:
            item["year"] = key[1]
        clean.append(item)
        if len(clean) >= max_items:
            break
    return clean

def format_context_block(contexts, limit=6):
    """Ajoute un en-tête [Source, Année] avant chaque extrait pour inciter la synthèse multi-sources."""
    formatted = []
    for c in contexts[:limit]:
        text = (c.get("text") or "").strip()
        if not text:
            continue
        src = (c.get("source") or c.get("org") or "").strip()
        yr  = (c.get("year") or "").strip()
        if src and yr and yr != "NC":
            head = f"[{src}, {yr}]"
        elif src:
            head = f"[{src}]"
        else:
            head = ""
        formatted.append((head + "\n" + text) if head else text)
    return "\n\n---\n\n".join(formatted)

# ========= Routes =========
@app.route("/", methods=["GET"])
def root():
    return redirect("/widget.html", code=302)

@app.route("/healthz", methods=["GET"])
def healthz():
    try:
        faiss_items = len(metadata) if metadata else 0
    except Exception:
        faiss_items = 0
    return jsonify({
        "ok": True,
        "time_utc": datetime.datetime.utcnow().isoformat()+"Z",
        "faiss_loaded": bool(index),
        "faiss_items": faiss_items,
        "model": OPENAI_CHAT_DEPLOYMENT_NAME,
        "embeddings": OPENAI_EMBEDDING_DEPLOYMENT,
        "daily_ask_limit": DAILY_ASK_LIMIT
    })

@app.route("/ask", methods=["POST"])
def ask():
    t0 = time.time()
    ip_h = ip_hash()

    # Limitation 3 questions / jour (UTC) — avant tout appel coûteux
    if not can_ask_today(ip_h):
        send_make({
            "date": datetime.datetime.utcnow().isoformat(),
            "ts": int(time.time()),
            "ip_hash": ip_h,
            "country": get_country(),
            "rate_limited": True
        })
        return jsonify({"error": "Limite atteinte : 3 questions par jour", "remaining": 0}), 429

    try:
        data = request.get_json(force=True)
        question = (data.get("question") or "").strip()
        history  = data.get("history") or []
        top_k    = int(data.get("top_k") or 6)
        top_k    = max(1, min(12, top_k))
        if not question:
            return jsonify({"error": "Missing 'question'"}), 400

        # RAG: recherche multi-sources
        contexts, _ = semantic_search(
            client=client,
            query=question,
            index=index,
            metadata=metadata,
            top_k=top_k,
            embedding_deploy=OPENAI_EMBEDDING_DEPLOYMENT
        )

        # Contexte formaté & citations propres
        context_block = format_context_block(contexts, limit=top_k)
        citations = build_citations(contexts, max_items=5)

        # Chat
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for turn in history[:10]:
            r, c = turn.get("role"), (turn.get("content") or "")[:1200]
            if r in ("user", "assistant") and c:
                messages.append({"role": r, "content": c})

        user_msg = (
            "Rédige une réponse unique, structurée et synthétique (≤150 mots), "
            "en croisant les extraits pertinents ci-dessous. "
            "Ne liste pas les sources au fil du texte; synthétise d’abord, "
            "puis termine par une ligne de références au format: "
            "Références: [Org, Année]; [Org2, Année2].\n\n"
            f"Context:\n{context_block}\n\nQuestion: {question}"
        )
        messages.append({"role": "user", "content": user_msg})

        resp = client.chat.completions.create(
            model=OPENAI_CHAT_DEPLOYMENT_NAME,
            messages=messages,
            temperature=0.2,
            max_tokens=500
        )
        answer = resp.choices[0].message.content.strip()

        # Nettoyage (numéros [1], disclaimers éventuels)
        answer = re.sub(r'\s*\[(\d{1,3})\]\s*', ' ', answer)
        answer = re.sub(r'(This content is for guidance only.*?medical product\.)', '', answer, flags=re.I|re.S)
        answer = re.sub(r'(Ce contenu est fourni.*?dispositif médical\.)', '', answer, flags=re.I|re.S)
        answer = re.sub(r'\n{3,}', '\n\n', answer).strip()

        # Si pas de ligne "Références:" en fin de texte, on l'ajoute
        if "Références:" not in answer:
            refs_txt = "; ".join(
                [f"[{c['source']}" + (f", {c['year']}]" if 'year' in c else "]") for c in citations]
            )
            if refs_txt:
                answer = f"{answer}\n\nRéférences: {refs_txt}"

        # Metrics & webhook
        latency_ms = int((time.time() - t0) * 1000)
        fallback = is_gpt_fallback(contexts, answer)
        mark_counts(fallback)
        try:
            send_make({
                "date": datetime.datetime.utcnow().isoformat(),
                "ts": int(time.time()),
                "ip_hash": ip_h,
                "country": get_country(),
                "latency_ms": latency_ms,
                "time_run": latency_ms,
                "model": OPENAI_CHAT_DEPLOYMENT_NAME,
                "answer_source": "fallback" if fallback else "corpus",
                "gpt_flag": "🚩" if fallback else "",
                "user_day": len(SEEN_IPS),
                "gpt_fallback_pct": round((FALLBACK_COUNT / TOTAL_REQUESTS) * 100, 2) if TOTAL_REQUESTS else 0.0,
                "satisfaction": ""
            })
        except Exception:
            pass

        return jsonify({
            "answer": answer,
            "citations": citations
        })

    except Exception as e:
        try:
            send_make({
                "date": datetime.datetime.utcnow().isoformat(),
                "ts": int(time.time()),
                "ip_hash": ip_h,
                "country": get_country(),
                "error": str(e)
            })
        except Exception:
            pass
        return jsonify({"error": str(e)}), 500

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json(force=True)
    sig = (data.get("signal", "").lower())
    if sig not in ("up", "down"):
        sig = ""  # vide = absence de pouce
    send_make({
        "date": datetime.datetime.utcnow().isoformat(),
        "ts": int(time.time()),
        "ip_hash": ip_hash(),
        "country": get_country(),
        "satisfaction": sig
    })
    return jsonify({"ok": True})

@app.route("/widget.html", methods=["GET"])
def serve_widget():
    path = os.path.join(app.root_path, "widget.html")
    if not os.path.exists(path):
        return make_response("widget.html not found at: " + path, 404)
    return send_file(path, mimetype="text/html")

if __name__ == "__main__":
    # PORT peut venir d'Azure App Service ou local
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))







