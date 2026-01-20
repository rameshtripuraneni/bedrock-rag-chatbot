from fastapi import FastAPI
from src.db import init_db
from src.schemas import ChatRequest, ChatResponse, IngestRequest
from src.rag import answer
from src.ingest import ingest_document

app = FastAPI(title="Bedrock RAG Chatbot")

@app.on_event("startup")
def _startup():
    init_db()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/ingest")
def ingest(req: IngestRequest):
    doc_id = ingest_document(req.source, req.content)
    return {"document_id": doc_id}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    out = answer(req.query)
    return ChatResponse(**out)
