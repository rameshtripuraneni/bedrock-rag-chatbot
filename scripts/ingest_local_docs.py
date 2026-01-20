from pathlib import Path
from src.db import init_db
from src.ingest import ingest_document

def main():
    init_db()
    base = Path("data/sample_docs")
    for p in base.glob("*"):
        if p.is_file():
            content = p.read_text(encoding="utf-8", errors="ignore")
            ingest_document(source=str(p), content=content)
            print("Ingested:", p)

if __name__ == "__main__":
    main()
