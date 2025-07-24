import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from fastapi.testclient import TestClient
from monorepo.backend.app import app

client = TestClient(app)

def test_markers_endpoint():
    resp = client.get("/api/v1/markers")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_feedback_endpoint():
    resp = client.post("/api/v1/feedback", json={"analysis_id": "1", "message": "ok"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "received"
