from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from src.settings import settings

engine: Engine = create_engine(settings.database_url, pool_pre_ping=True)

def init_db() -> None:
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS documents (
              id SERIAL PRIMARY KEY,
              source TEXT NOT NULL,
              content TEXT NOT NULL
            );
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS chunks (
              id SERIAL PRIMARY KEY,
              document_id INT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
              chunk_index INT NOT NULL,
              content TEXT NOT NULL,
              embedding vector(1536) NOT NULL
            );
        """))
        conn.execute(text("CREATE INDEX IF NOT EXISTS chunks_embedding_idx ON chunks USING ivfflat (embedding vector_cosine_ops);"))
