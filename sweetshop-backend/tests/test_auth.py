from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    payload = {
        "name": "Test_Register_User",
        "email": "Testregister@gmail.com",
        "password": "testregister1"
    }
    response = client.post("/api/auth/register", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == "Test_Register_User"
    assert data["email"] == "testregister@gmail.com"
    assert "id" in data


def test_login_user():
    register_payload = {
        "name": "Test_LoginUser",
        "email": "Testlogin@gmail.com",
        "password": "testlogin1"
    }

    client.post("/api/auth/register", json=register_payload)

    login_payload = {
        "email": "testlogin@gmail.com",
        "password": "testlogin1"
    }

    response = client.post("/api/auth/login", json=login_payload)

    assert response.status_code == 200
    data = response.json()

    assert data["email"] == "testlogin@gmail.com"
    assert "token" in data
