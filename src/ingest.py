from sqlalchemy import text
from src.db import engine
from src.bedrock import embed_text
from src.utils.chunking import chunk_text
from src.settings import settings

def ingest_document(source: str, content: str) -> int:
    chunks = chunk_text(content, settings.chunk_size, settings.chunk_overlap)
    if not chunks:
        raise ValueError("No content to ingest")

    with engine.begin() as conn:
        doc_id = conn.execute(
            text("INSERT INTO documents(source, content) VALUES (:s, :c) RETURNING id"),
            {"s": source, "c": content},
        ).scalar_one()

        for i, ch in enumerate(chunks):
            emb = embed_text(ch)
            conn.execute(
                text("""
                  INSERT INTO chunks(document_id, chunk_index, content, embedding)
                  VALUES (:d, :i, :c, :e)
                """),
                {"d": doc_id, "i": i, "c": ch, "e": emb},
            )
    return doc_id
