# 🎥 YouTube Chat Bot

A **Streamlit + FastAPI** application that lets you **chat with YouTube videos** using **RAG (Retrieval-Augmented Generation)** with LangChain and FAISS.

Users can:

* Paste a YouTube URL
* Load the video transcript
* Ask questions about the video
* Get answers from a **vector-based RAG system**

---

## Screenshot

<img width="1901" height="930" alt="3Capture" src="https://github.com/user-attachments/assets/85dd0513-c4ea-45e7-a3b4-77d7ae8278fa" />

## 🗂 Project Structure

```
yt_chat_bot/
│
├── backend/
│   ├── main.py              # FastAPI app
│   ├── services.py          # Transcript loading + RAG functions
│   ├── requirements.txt
│   └── vectorstore/          # Saved FAISS embeddings (ignored in git)
│
├── frontend/
│   ├── app.py               # Streamlit UI
│   └── requirements.txt
│
├── .env             # API keys, credentials (DO NOT PUSH)
│
├── README.md
└── .gitignore
```

---

## ⚙️ Setup

### 1. Backend

```bash
cd backend
python -m venv venv
# Activate virtual environment
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt

# Run FastAPI
uvicorn main:app --reload --port 8000
```

The API will run at `http://localhost:8000`.

---

### 2. Frontend (Streamlit)

```bash
cd frontend
python -m venv venv
# Activate virtual environment
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py
```

Open the Streamlit app in your browser, usually at `http://localhost:8501`.

---

## ⚡ Features

* Extracts **YouTube video transcripts** automatically
* Splits transcript into **chunks** for better retrieval
* Builds **FAISS vector database** for semantic search
* Uses **Google Gemini** for llm and **HuggingFace embeddings** for RAG
* Simple **chat interface** in Streamlit

---

## 📝 Notes

* **Only one video at a time** is supported. The vectorstore is cleared on new video upload.
* Keep your API keys in `.env` and do **not** push them to GitHub.
* Vectorstore folder (`vectorstore/`) is **ignored** by git.

---

## 🛠 Requirements

* Python 3.10+
* FastAPI
* Streamlit
* LangChain
* youtube-transcript-api
* FAISS
* HuggingFace / Google Gemini embeddings

---

## 📌 License

MIT License



