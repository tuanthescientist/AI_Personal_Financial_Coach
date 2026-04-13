from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_spending_summary():
    response = client.get("/api/v1/spending/user_123")
    assert response.status_code == 200
    data = response.json()
    assert "total_spent" in data
    assert "total_income" in data
    assert "insights" in data
