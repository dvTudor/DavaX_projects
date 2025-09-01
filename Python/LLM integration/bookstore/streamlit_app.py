import tempfile
from openai import OpenAI
from rag import build_or_update_index, retrieve
from tools import get_summary_by_title
import streamlit as st
from pathlib import Path
import json
import base64
import os

MODEL = os.environ.get("CHAT_MODEL", "gpt-4o-mini")
# TTS_MODEL = os.environ.get("TTS_MODEL", "tts-1")
# IMAGES_MODEL = os.environ.get("IMAGES_MODEL", "dall-e-3")
# TRANSCRIBE_MODEL = os.environ.get("TRANSCRIBE_MODEL", "gpt-4o-transcribe")

BAD_WORDS = {"dark"}
def contains_bad_language(text: str) -> bool:
    t = text.lower()
    return any(b in t for b in BAD_WORDS)

# config page first
st.set_page_config(page_title="Smart Librarian")

# check API key
if not os.environ.get("OPENAI_API_KEY"):
    st.error("OPENAI_API_KEY variable is undefined.")
    st.stop()

client = OpenAI()

# index is built only once per session
if "index_built" not in st.session_state:
    build_or_update_index()
    st.session_state["index_built"] = True

st.title("Smart Librarian - RAG + Tool Completion")

q = st.text_input("Question (for example, \"I want a book about friendship and magic\")")
col1, col2, col3, col4 = st.columns(4)
speak = col1.checkbox("Text to Speech (mp3)")
use_audio = col2.checkbox("Use audio (transcribe)")
mk_image = col3.checkbox("Representative Image")
topk = col4.slider("Top-K RAG", 1, 5, 3)

audio_file = None
if use_audio:
    audio_file = st.file_uploader(
        "Upload an audio file (mp3, wav)",
        type=["mp3", "wav"],
        accept_multiple_files=False,
    )
    if audio_file is not None:
        st.audio(audio_file)

def tool_schema():
    return [{
        "type": "function",
        "function": {
            "name": "get_summary_by_title",
            "description": "Return complete summary for a specific title",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Exact title of the book"}
                },
                "required": ["title"]
            }
        }
    }]

# def transcribe_uploaded_audio(upload):
#     if upload is None:
#         return None

#     suffix = os.path.splitext(upload.name or "audio")[1] or ".mp3"

#     with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
#         tmp.write(upload.getbuffer())
#         tmp.flush()
#         tmp_path = tmp.name
#     try:
#         with open(tmp_path, "rb") as f:
#             tr = client.audio.transcriptions.create(model=TRANSCRIBE_MODEL, file=f)
#         return getattr(tr, "text", "").strip()
#     finally:
#         try:
#             os.remove(tmp_path)
#         except Exception:
#             pass

if st.button("Search & Recommend") and q:
    # # determine the query: prefer audio transcription when provided
    # q = None
    #
    # if use_audio and audio_file is not None:
    #     with st.spinner("Transcribing audio…"):
    #         try:
    #             q = transcribe_uploaded_audio(audio_file)
    #         except Exception as e:
    #             st.error(f"Transcription error: {e}")
    #             st.stop()
    #
    #     if not q:
    #         st.warning("Could not obtain audio transcription. Try with another file or use the text field.")
    #         st.stop()
    #
    #     st.success("Audio transcribed.")
    #
    #     with st.expander("Text transcribed"):
    #         st.write(q)
    #
    # else:
    #     q = q_text
    # if not q:
    #     st.warning("Complete the question or upload an audio file.")
    #     st.stop()

    if contains_bad_language(q):
        st.warning("Watch your mouth!")
        st.stop()

    # RAG retrieval
    try:
        hits = retrieve(q, top_k=topk)
    except Exception as e:
        st.error(f"Error during retrieval: {e}")
        st.stop()

    if not hits:
        st.warning("No relevant titles found. Please try rephrasing your question.")
        st.stop()

    with st.expander("RAG Candidates"):
        for h in hits:
            st.write(f"**{h['title']}** · themes: {', '.join(h.get('themes', []))} · score={h['score']:.3f}")
            st.caption(h["short_summary"])

    # build the prompt
    cand_text = "\n".join([
        f"- {h['title']} | {', '.join(h.get('themes', []))} | {h['short_summary']}"
        for h in hits
    ])
    messages = [
        {
            "role": "system",
            "content": (
                "You are a smart librarian. Pick exactly one book from the list of candidates.\n"
                "After deciding on an entry, call get_summary_by_title(title) for the full summary.\n"
                "Respond conversationally in English and list 2-3 reasons (themes) for your choice."
            )
        },
        {"role": "system", "content": f"Candidates:\n{cand_text}"},
        {"role": "user", "content": q},
    ]

    # first call to the model
    try:
        first = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tool_schema(),
            tool_choice={"type": "function", "function": {"name": "get_summary_by_title"}},
            parallel_tool_calls=False,
            temperature=0.3
        )
    except Exception as e:
        st.error(f"Error upon calling the model: {e}")
        st.stop()

    tool_msgs = []
    first_msg = first.choices[0].message

    # call tools
    if getattr(first_msg, "tool_calls", None):
        for tc in first_msg.tool_calls:
            if tc.type == "function":
                name = tc.function.name
                args = json.loads(tc.function.arguments or "{}")
                try:
                    result = get_summary_by_title(args["title"])
                except Exception as e:
                    result = f"ERROR: {e}"
                tool_msgs.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "name": name,
                    "content": result
                })

        # second call to the model
        try:
            final = client.chat.completions.create(
                model=MODEL,
                messages=messages + [first_msg] + tool_msgs,
                temperature=0.3
            )
            answer = final.choices[0].message.content
        except Exception as e:
            st.error(f"Error upon calling the model: {e}")
            st.stop()

        st.markdown("### Recommendation")
        st.write(answer)
        st.stop()

    else:
        # fallback mechanism: manually pick a candidate and add extra context
        try:
            fallback_title = hits[0]["title"]
            fallback_result = get_summary_by_title(fallback_title)
            final_messages = messages + [
                first_msg,
                {
                    "role": "system",
                    "content": (
                        f"Additional context: Full summary for '{fallback_title}'. "
                        f"Use it to compose the final answer:\n\n{fallback_result}"
                    )
                }
            ]
        except Exception as e:
            st.error(f"Error upon calling fallback tool: {e}")
            st.stop()

        # second call to the model again
        try:
            final = client.chat.completions.create(
                model=MODEL,
                messages=final_messages,
                temperature=0.3
            )
            answer = final.choices[0].message.content
        except Exception as e:
            st.error(f"Error upon calling model: {e}")
            st.stop()

        st.markdown("### Recommendation")
        st.write(answer)
        st.stop()

    # if mk_image:
    #     try:
    #         title = hits[0]["title"]
    #         prompt = f"Minimalist book-cover style image inspired by '{title}' and themes: {', '.join(hits[0].get('themes', []))}."
    #         img = client.images.generate(model=IMAGES_MODEL, prompt=prompt, size="1024x1024")
    #         b64 = img.data[0].b64_json
    #         st.image(base64.b64decode(b64), caption=f"Suggested cover: {title}")
    #     except Exception as e:
    #         st.error(f"Error upon generating image: {e}")

    # if speak:
    #     try:
    #         out = Path("out")
    #         out.mkdir(exist_ok=True)
    #         mp3_path = out / "recommendation.mp3"
    #         with client.audio.speech.with_streaming_response.create(
    #             model=TTS_MODEL, voice="alloy", input=answer
    #         ) as response:
    #             response.stream_to_file(str(mp3_path))
    #         with mp3_path.open("rb") as f:
    #             st.download_button("Download MP3", data=f, file_name="recommendation.mp3")
    #     except Exception as e:
    #         st.error(f"Error upon TTS: {e}")
