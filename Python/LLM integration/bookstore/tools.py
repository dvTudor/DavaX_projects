from typing import Dict
import json
from functools import lru_cache
from pathlib import Path

DATA_PATH = Path("data/book_summaries.json")

@lru_cache(maxsize=1)
def _load() -> Dict[str, str]:
    with DATA_PATH.open("r", encoding="utf-8") as f:
        books = json.load(f)

    return {b["title"]: b["long_summary"] for b in books}

def get_summary_by_title(title: str) -> str:
    summaries = _load()

    if title in summaries:
        return summaries[title]
    
    wanted = title.strip().lower()
    for k, v in summaries.items():
        if k.lower() == wanted:
            return v
        
    raise ValueError(f'Title not found: {title}')