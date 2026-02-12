from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_rag_ingest_and_query():
    ingest = {
        "doc_id": "doc_test_1",
        "doc_type": "SOP",
        "content": "If crowd density is high, escalate to supervisor and deploy barricades.",
        "metadata": {"topic": "crowd"}
    }
    r1 = client.post("/api/v1/documents/ingest", json=ingest)
    assert r1.status_code == 200

    q = {"query": "What to do in high crowd density?", "k": 2, "filters": {}}
    r2 = client.post("/api/v1/rag/query", json=q)
    assert r2.status_code == 200
    out = r2.json()
    assert out["query"]
    assert isinstance(out["results"], list)
