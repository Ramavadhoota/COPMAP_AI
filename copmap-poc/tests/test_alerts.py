from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_create_alert():
    payload = {
        "type": "crowd_density",
        "priority": "P2",
        "lat": 12.9716,
        "lon": 77.5946,
        "confidence": 0.9,
        "metadata": {"person_count": 100}
    }
    r = client.post("/api/v1/alerts", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["type"] == "crowd_density"
    assert data["priority"] == "P2"
