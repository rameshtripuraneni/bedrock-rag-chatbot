from src.utils.chunking import chunk_text

def test_chunking_basic():
    t = "a" * 1000
    chunks = chunk_text(t, chunk_size=200, overlap=50)
    assert len(chunks) > 1
    assert chunks[0] == "a" * 200
