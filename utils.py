import faiss
import json
import os
import numpy as np

def load_faiss(index_path: str, metadata_path: str):
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"FAISS index not found: {index_path}")
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Metadata not found: {metadata_path}")
    index = faiss.read_index(index_path)
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return index, metadata

def _norm_source(meta_item: dict):
    # Essaye de normaliser une citation sous forme [Organization, Year]
    org = (meta_item.get("organization") or meta_item.get("source") or "NC").strip()
    year = (meta_item.get("year") or "NC").strip()
    # Nettoyage fréquent (nom de fichier -> label court)
    org = org.replace(".pdf","").replace("_"," ").strip()
    # Raccourcis usuels
    map_org = {
        "sign": "SIGN",
        "nice": "NICE",
        "has": "HAS"
    }
    low = org.lower()
    for k,v in map_org.items():
        if k in low and len(org) <= 12:
            org = v
            break
    return {"source": org, "year": year}

def semantic_search(client, query: str, index, metadata, top_k=6, embedding_deploy=""):
    # 1) Embedding de la requête
    emb = client.embeddings.create(model=embedding_deploy, input=query).data[0].embedding
    vec = np.array(emb, dtype=np.float32)[None, :]

    # 2) Recherche FAISS
    scores, ids = index.search(vec, top_k)
    ids = ids[0].tolist()

    # 3) Récupère extraits + meta
    contexts, citations = [], []
    for idx in ids:
        if idx < 0: 
            continue
        m = metadata[str(idx)] if isinstance(metadata, dict) and str(idx) in metadata else metadata[idx]
        text = (m.get("text") or "")[:1200]
        contexts.append({"text": text})
        citations.append(_norm_source(m))
    return contexts, citations

