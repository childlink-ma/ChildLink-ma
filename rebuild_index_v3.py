import os, json, time, re
import numpy as np, faiss
from tqdm import tqdm
from openai import AzureOpenAI

DIMS   = int(os.getenv("EMBEDDING_DIM", "1536"))
DEPLOY = os.getenv("OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")
APIVER = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version=APIVER,
)

def load_chunks():
    # on utilise le fichier enrichi
    path = os.getenv("FAISS_METADATA_PATH", "chunks_enriched.json")
    if not os.path.exists(path):
        path = "chunks_enriched.json"
    if not os.path.exists(path):
        raise FileNotFoundError("chunks_enriched.json introuvable")

    data = json.load(open(path, "r", encoding="utf-8"))
    if isinstance(data, dict):
        # si jamais c'était encapsulé dans une clé
        for k,v in data.items():
            if isinstance(v, list):
                data = v; break

    rows = []
    for r in data:
        if not isinstance(r, dict): 
            continue
        text = (r.get("content") or "").strip()
        if not text:
            continue
        src = (r.get("source_pdf") or "").strip()

        # org = on n'a que la source pdf -> on garde le filename comme trace
        org = src if src else "NC"

        # year = première année (19xx/20xx) trouvée dans le filename puis le contenu
        year = "NC"
        for candidate in (src, text[:2000]):  # on limite le scan du contenu
            m = re.search(r'(?<!\d)(19|20)\d{2}(?!\d)', str(candidate))
            if m:
                year = m.group(0)
                break

        rows.append({"text": text, "org": org, "year": year, "topic": "NC"})
    return rows

def embed_batch(texts):
    resp = client.embeddings.create(model=DEPLOY, input=texts, dimensions=DIMS)
    return np.array([d.embedding for d in resp.data], dtype="float32")

def main():
    rows = load_chunks()
    n = len(rows)
    print(f"Chunks: {n}")

    BATCH = 96
    vecs = np.zeros((n, DIMS), dtype="float32")

    t0 = time.time(); calls = 0
    for i in tqdm(range(0, n, BATCH)):
        if calls and calls % 30 == 0:
            dt = time.time() - t0
            if dt < 60: time.sleep(60 - dt)
            t0 = time.time()
        chunk = [r["text"] for r in rows[i:i+BATCH]]
        V = embed_batch(chunk)
        vecs[i:i+len(V)] = V
        calls += 1

    # cosine
    faiss.normalize_L2(vecs)
    index = faiss.IndexFlatIP(DIMS)
    index.add(vecs)

    faiss.write_index(index, "clm_index_v3.index")
    json.dump(rows, open("clm_metadata_v3.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump({"model": DEPLOY, "dims": DIMS, "n_vectors": n, "similarity":"cosine"},
              open("index_info_v3.json","w",encoding="utf-8"), indent=2)

    print("OK -> clm_index_v3.index / clm_metadata_v3.json / index_info_v3.json")

if __name__ == "__main__":
    main()
