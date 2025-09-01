from openai import OpenAI
from typing import Any, Dict, List
import os
from tools import get_summary_by_title
from rag import build_or_update_index, retrieve
import pathlib
import base64
import sys
import json
from pathlib import Path 

MODEL = os.environ.get("CHAT_MODEL", "gpt-4o-mini")
OUT_DIR = Path("output")

client = OpenAI()

BAD_WORDS = {"dark"}
def contains_bad_language(text: str) -> bool:
    t = text.lower()
    return any(b in t for b in BAD_WORDS)

def make_tools_schema() -> List[Dict[str, Any]]:
    return [{
        "type": "function",
        "function": {
            "name": "get_summary_by_title",
            "description": "Return the full summary for an exact book title.",
            "parameters": {
                "type":"object",
                "properties": {
                    "title": {
                        "type":"string",
                        "description": "Exact book title"
                    }
                },
                "required": ["title"]
            }
        }
    }]

def call_tool(name: str, arguments: Dict[str, Any]) -> str:
    if name == "get_summary_by_title":
        return get_summary_by_title(arguments["title"])
    raise RuntimeError(f"Unknown tool: {name}")
if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    count = build_or_update_index()
    print(f"[init] Indexed documents in Chroma: {count}")

    question = input("Question: ").strip()

    if contains_bad_language(question):
        print("Watch your mouth!")
        sys.exit(0)

    hits = retrieve(question, top_k=4)
    candidates_txt = "\n".join([
        f"- {h['title']} | teme: {', '.join(h.get('themes', []))} | scurt: {h['short_summary']} (score={h['score']:.3f})"
        for h in hits
    ])

    system = {
        "role": "system",
        "content": (
            "You are a smart librarian. Pick exactly one book from the list of candidates.\n"
            "After deciding on an entry, call get_summary_by_title(title) for the full summary.\n"
            "Respond conversationally in English and list 2-3 reasons (themes) for your choice."
        )
    }

    user = {"role":"user","content": question}

    context = {
        "role": "system",
        "content": f"Top k candidates:\n{candidates_txt}\nPick only from these titles."
    }

    first = client.chat.completions.create(
        model=MODEL,
        messages=[system, context, user],
        tools=make_tools_schema(),
        tool_choice="auto",
        temperature=0.3
    )

    tool_messages: List[Dict[str, Any]] = []
    
    first_msg = first.choices[0].message
    if getattr(first_msg, "tool_calls", None):
        for tc in first_msg.tool_calls:
            if tc.type == "function":
                name = tc.function.name
                args = json.loads(tc.function.arguments or "{}")
                try:
                    result = call_tool(name, args)
                except Exception as e:
                    result = f"ERROR: {e}"
                tool_messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "name": name,
                    "content": result
                })

    # produce final answer with tool output included
    final = client.chat.completions.create(
        model=MODEL,
        messages=[system, context, user, first_msg] + tool_messages,
        temperature=0.4
    )

    answer = final.choices[0].message.content
    print("\n=== Recommendation ===\n")
    print(answer)
    