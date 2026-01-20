
# bedrock-rag-chatbot
chat bot

# Bedrock RAG Chatbot (Postgres + pgvector)

A production-style Retrieval Augmented Generation (RAG) service using:
- Amazon Bedrock (embeddings + chat model)
- Postgres + pgvector for vector search (local dev via docker-compose)
- FastAPI for API
- Clean code structure + tests + CI

## Architecture (local)
Client -> FastAPI -> (embed/query via Bedrock) -> Postgres(pgvector) -> RAG prompt -> Bedrock chat model -> response

## Prereqs
- Python 3.11+
- Docker
- AWS credentials in your environment (for Bedrock access)

## Setup
```bash
cp .env.example .env
docker compose up -d
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e .
```

## Ingest sample docs
```bash
python scripts/ingest_local_docs.py
```

## Run API
```bash
uvicorn src.app:app --reload --port 8000
```

## Chat
```bash
curl -s -X POST http://localhost:8000/chat       -H "Content-Type: application/json"       -d '{"query":"What is this project about?"}'
```

## Notes
- Replace Bedrock model IDs in `.env` based on your account access.
- Some Bedrock model request/response formats differ. Adjust `src/bedrock.py` if needed.
- For deployment you can move FastAPI behind API Gateway + Lambda (Mangum) or ECS.

