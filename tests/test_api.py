from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict_endpoint():
    payload = {
        "sample": {
            "fixed_acidity": 7.0,
            "volatile_acidity": 0.27,
            "citric_acid": 0.36,
            "residual_sugar": 20.7,
            "chlorides": 0.045,
            "free_sulfur_dioxide": 45.0,
            "total_sulfur_dioxide": 170.0,
            "density": 1.001,
            "ph": 3.0,
            "sulphates": 0.45,
            "alcohol": 8.8
        },
        "model_input": {
            "model_path": "/home/jan/wine-quality-prediction/models/rf.pkl"
        }
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert isinstance(response.json()['quality_prediction'], (int, float))

def test_auth_protected_route():
    response = client.get("/secure")
    assert response.status_code == 401

def test_register_and_login():
    email = "test@example.com"
    password = "test1234"

    # Registrierung
    r = client.post("/register", json={"email": email, "password": password})
    assert r.status_code in [200, 400]  # User könnte schon existieren

    # Login
    r = client.post("/token", data={"username": email, "password": password})
    assert r.status_code == 200
    assert "access_token" in r.json()
