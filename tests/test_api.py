import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert "version" in body


def test_spending_summary():
    resp = client.get("/api/v1/spending/demo_user_001", params={"days": 30})
    assert resp.status_code == 200
    data = resp.json()
    assert "total_income" in data
    assert "total_expenses" in data
    assert "savings_rate" in data
    assert "categories" in data
    assert isinstance(data["categories"], list)
    assert "insights" in data


def test_spending_invalid_days():
    resp = client.get("/api/v1/spending/demo_user_001", params={"days": 3})
    assert resp.status_code == 422  # validation error


def test_goals_crud():
    # Create
    resp = client.post("/api/v1/goals/", json={
        "user_id": "test_user",
        "goal_name": "Emergency Fund",
        "target_amount": 50_000_000,
    })
    assert resp.status_code == 201
    goal = resp.json()
    assert goal["goal_name"] == "Emergency Fund"

    # List
    resp = client.get("/api/v1/goals/test_user")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1
