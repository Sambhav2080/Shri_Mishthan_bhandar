from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    payload = {
        "name": "Sambhav",
        "email": "sambhavoct2004@gmail.com",
        "password": "password123"
    }
    response = client.post("/api/auth/register", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == "Sambhav"
    assert data["email"] == "sambhavoct2004@gmail.com"
    assert "id" in data


def test_login_user():
    register_payload = {
        "name": "SambhavK",
        "email": "sambhavoct2003@gmail.com",
        "password": "password123"
    }

    client.post("/api/auth/register", json=register_payload)

    login_payload = {
        "email": "sambhavoct2003@gmail.com",
        "password": "password123"
    }

    response = client.post("/api/auth/login", json=login_payload)

    assert response.status_code == 200
    data = response.json()

    assert data["email"] == "sambhavoct2003@gmail.com"
    assert "token" in data
