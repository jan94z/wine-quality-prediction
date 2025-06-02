import os
# SET TEST ENVIRONMENT VARIABLES
os.environ["POSTGRES_USER"] = "postgres"
os.environ["POSTGRES_PASSWORD"] = "postgres"
os.environ["POSTGRES_HOST"] = "localhost"
os.environ["POSTGRES_PORT"] = "5433" 
os.environ["POSTGRES_DB"] = "db"
os.environ["MLFLOW_URI"] = "http://localhost:5000"
os.environ["CRYPT_CONTEXT"] = "bcrypt"
os.environ["TEST_USER"] = "test_user@test.com"
os.environ["TEST_PASSWORD"] = "test_password"
os.environ["JWT_SECRET_KEY"] = "test_key"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"

from fastapi.testclient import TestClient
from api.main import app
import pytest
from sqlalchemy import text
from shared.utils import get_engine, query
import numpy as np

### BASIC TESTS ###
# API #
client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict_endpoint():
    login_response = client.post("/token", data = {"username": os.environ["TEST_USER"], "password": os.environ["TEST_PASSWORD"]})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    payload = {
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
        }


    response = client.post("/predict", json=payload, headers=headers)
    assert response.status_code == 200
    # TODO CHECK MODEL FUNCTIONALITY, EASIER HERE BECAUSE I LOAD A MODEL ANYWAY
    prediction = response.json()['quality_prediction']
    assert isinstance(prediction[0], (int, np.integer))
    assert 0 <= prediction[0] <= 10

# def test_auth_protected_route():
#     response = client.get("/secure")
#     assert response.status_code == 401

def test_register_and_login():
    email = "test@example.com"
    password = "test1234"

    # Registrierung
    r = client.post("/register", json={"email": email, "password": password})
    assert r.status_code in [200, 400]  # User could already exist

    # Login
    r = client.post("/token", data={"username": email, "password": password})
    assert r.status_code == 200
    assert "access_token" in r.json()


# DB 
@pytest.fixture(scope="module")
def test_db():
    engine = get_engine()
    # create table for testing
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS test_users (
                id SERIAL PRIMARY KEY,
                username TEXT,
                password TEXT
            )
        """))
        conn.execute(text("INSERT INTO test_users (username, password) VALUES ('test', 'test')"))

    yield engine

    # drop table after tests
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS test_users"))

def test_user_insert(test_db):
    with test_db.connect() as conn:
        result = conn.execute(text("SELECT * FROM test_users WHERE username='test'"))
        row = result.fetchone()
        assert row is not None
        assert row.username == 'test'
