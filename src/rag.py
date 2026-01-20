from sqlalchemy import text
from src.db import engine
from src.bedrock import embed_text, chat_complete
from src.settings import settings

def retrieve(query: str, top_k: int) -> list[dict]:
    q_emb = embed_text(query)
    with engine.begin() as conn:
        rows = conn.execute(
            text("""
              SELECT c.content, d.source
              FROM chunks c
              JOIN documents d ON d.id = c.document_id
              ORDER BY c.embedding <=> :q
              LIMIT :k
            """),
            {"q": q_emb, "k": top_k},
        ).mappings().all()
    return [dict(r) for r in rows]

def answer(query: str) -> dict:
    hits = retrieve(query, settings.top_k)
    context_parts = []
    for h in hits:
        context_parts.append(f"[source={h['source']}]\n{h['content']}\n")
    context = "\n---\n".join(context_parts)
    context = context[: settings.max_context_chars]

    system = (
        "You are a helpful assistant. Answer using ONLY the provided context. "
        "If the answer is not in the context, say you don't know. "
        "Include brief citations like (source: X)."
    )
    user = f"CONTEXT:\n{context}\n\nQUESTION:\n{query}\n\nAnswer:"
    response = chat_complete(system=system, user=user)
    return {"answer": response, "sources": list({h["source"] for h in hits})}
