# Smart Librarian – RAG + Tool Completion

An AI-powered book recommendation system that combines OpenAI GPT models with Retrieval-Augmented Generation (RAG) using ChromaDB.  
The chatbot recommends books based on user interests (themes, keywords, or questions) and elaborates on the recommendation with a detailed summary retrieved through a custom tool.

---

## Features

- **Book database**: `book_summaries.json` includes 10 classic books with themes, short summaries and longer summaries.
- **Vector search with RAG**:  
  Uses OpenAI embeddings (`text-embedding-3-small`) and ChromaDB for semantic retrieval.
- **Chatbot interaction**:  
  - Accepts text queries (`"I want a book about friendship and magic"`).  
  - Retrieves top-k candidates.  
  - GPT model picks the best recommendation and explains the choice.  
- **Tool calling (`get_summary_by_title`)**:  
  After selecting a book, the chatbot calls a registered function to return the full summary.
- **Bad language filter**: Politely rejects offensive input.
- **Interfaces**:  
  - **CLI** (`app.py`) – interactive console chatbot.  
  - **Streamlit app** (`streamlit_app.py`) – web-based UI with optional TTS, speech-to-text, and image generation (commented for optional use).

---

## Project Structure

```
├── app.py                # CLI chatbot implementation
├── streamlit_app.py      # Streamlit-based chatbot UI
├── rag.py                # RAG logic: embeddings, ChromaDB indexing, retrieval
├── tools.py              # Tool: get_summary_by_title
├── data/                 # Data directory (used by tools & RAG)
│   └── book_summaries.json
├── requirements.txt      # required packages
```

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone <repo-url>
cd <your-repo-folder>
```

### 2. Create and activate a virtual environment
```bash
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
.venv/Scripts/Activate.ps1 # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set environment variables
```bash
export OPENAI_API_KEY="your_api_key_here"
export CHAT_MODEL="gpt-4o-mini"
```

(Optionally: `TTS_MODEL`, `IMAGES_MODEL`, `TRANSCRIBE_MODEL` if you enable those features in Streamlit.)

---

## Running the Project

### Option A – Command-line interface
```bash
python app.py
```
- Prompts for a question in the terminal.  
- Returns one recommended book + detailed summary.

### Option B – Streamlit interface
```bash
streamlit run streamlit_app.py
```
- Opens a web app in your browser.  
- Features:
  - Text query input
  - Optional audio upload (for transcription)
  - Optional Text-to-Speech
  - Optional book cover image generation

---

## Core Components

- **RAG Engine**:  
  - `rag.py` builds/updates the ChromaDB index and retrieves top-k relevant results.
- **Tool – Book Summaries**:  
  - `tools.py` implements `get_summary_by_title(title)` which loads `book_summaries.json` and returns the long summary.
- **Chatbot Flow**:  
  1. User submits a query.  
  2. Relevant books retrieved via RAG.  
  3. GPT model selects the best candidate.  
  4. Tool is called for the full summary.  
  5. Final recommendation is displayed.

---

## Example Queries

- *"I want a book about friendship and magic"*  
- *"What do you recommend for someone who enjoys war stories?"*  
- *"Give me something about freedom and social control"*  
- *"What is 1984?"*

---

## Optional Features (Streamlit Only)

- **Text-to-Speech**: Converts recommendations to audio (mp3).  
- **Speech-to-Text**: Allows vocal interaction (audio upload).  
- **Image Generation**: Produces a book-cover style image.  

*(These are currently commented out in `streamlit_app.py` since the guidelines were to use lower priced models.)*

---

## Dataset

The project includes 10 classic books (e.g., *1984*, *The Hobbit*, *Pride and Prejudice*, *Moby-Dick*), each with:
- Themes
- Short summary
- Long summary

---

## Notes

- Assignment requirements have been implemented.  
- Default vector store: ChromaDB.  
- For extensions, other frontend frameworks may be used (for example, React, Angular or Vue).

---

## Dependencies

Listed in `requirements.txt`:

```
openai
streamlit
chromadb
```
