from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services import load_transcript, query_rag

app = FastAPI()

# -------------------- CORS --------------------
origins = ["http://localhost:8501", "http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Models --------------------
class VideoRequest(BaseModel):
    url: str

class QuestionRequest(BaseModel):
    question: str

# -------------------- Endpoints --------------------
@app.post("/load_video/")
def load_video(req: VideoRequest):
    chunks = load_transcript(req.url)
    return {"status": "success", "chunks": chunks}

@app.post("/ask/")
def ask(req: QuestionRequest):
    answer = query_rag(req.question)
    return {"answer": answer}
