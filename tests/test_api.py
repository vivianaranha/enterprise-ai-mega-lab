from fastapi.testclient import TestClient
from backend.app.main import app

with TestClient(app) as client:
    def test_health():
        r=client.get("/health")
        assert r.status_code==200
        assert r.json()["status"]=="ok"

    def test_ask_agent():
        r=client.post("/agents/ask",json={"message":"Find the best sales opportunities"})
        assert r.status_code==200
        body=r.json()
        assert body["agent"]=="sales"
        assert body["data"]

    def test_knowledge_search():
        r=client.get("/knowledge/search",params={"q":"travel meal reimbursement"})
        assert r.status_code==200
        assert len(r.json())>0
