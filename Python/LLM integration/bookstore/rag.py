from typing import List, Dict, Any
from openai import OpenAI
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import json
import os
import pathlib

CHROMA_DIR = "db"
DATA_PATH = "data/book_summaries.json"
EMBED_MODEL = "text-embedding-3-small"

client = OpenAI() 

def _load_data() -> List[Dict[str, Any]]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def _ensure_collection():
    # ensure directory exists
    pathlib.Path(CHROMA_DIR).mkdir(parents=True, exist_ok=True)

    chroma = chromadb.PersistentClient(
        path=CHROMA_DIR,
        settings=Settings(allow_reset=False)
    )

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.environ.get("OPENAI_API_KEY"),
        model_name=EMBED_MODEL
    )

    try:
        col = chroma.get_collection("book_summaries", embedding_function=openai_ef)
    except Exception:
        col = chroma.create_collection(name="book_summaries", embedding_function=openai_ef)

    return chroma, col

def build_or_update_index() -> int:
    data = _load_data()
    _, col = _ensure_collection()

    existing = set(col.get()["ids"]) if col.count() > 0 else set()
    to_add = []
    for item in data:
        _id = item["title"]
        if _id not in existing:
            # sanitize metadata: lists to strings
            md = dict(item)
            if isinstance(md.get("themes"), list):
                md["themes"] = json.dumps(md["themes"], ensure_ascii=False)  # serialize list
            to_add.append(md)

    if to_add:
        col.add(
            ids=[d["title"] for d in to_add],
            documents=[
                d["short_summary"] + " Themes: " + (
                    ", ".join(json.loads(d["themes"])) if isinstance(d.get("themes"), str) and d["themes"].startswith("[")
                    else str(d.get("themes", ""))
                )
                for d in to_add
            ],
            metadatas=to_add
        )
    return col.count()

def retrieve(query: str, top_k: int = 4) -> List[Dict[str, Any]]:
    _, col = _ensure_collection()
    res = col.query(query_texts=[query], n_results=top_k, include=["metadatas", "distances", "documents"])

    hits = []
    if not res["ids"] or not res["ids"][0]:
        return hits

    for i in range(len(res["ids"][0])):
        meta = res["metadatas"][0][i]

        # parse themes back to list if encoded with JSON
        themes_val = meta.get("themes", [])
        if isinstance(themes_val, str):
            try:
                parsed = json.loads(themes_val)
                if isinstance(parsed, list):
                    themes_val = parsed
            except Exception:
                # fallback if it was stored as comma-separated string
                themes_val = [t.strip() for t in themes_val.split(",") if t.strip()]

        hits.append({
            "title": meta["title"],
            "themes": themes_val,
            "long_summary": meta["long_summary"],
            "short_summary": meta["short_summary"],
            "score": float(res["distances"][0][i]),
        })

    hits.sort(key=lambda x: x["score"])
    return hits
