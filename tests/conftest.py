import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

def test_health(client):
    response = client.get("/health")
    print(response.json())
    assert response.status_code == 200
