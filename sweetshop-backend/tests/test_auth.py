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
    assert "access_token" in data
    assert "refresh_token" in data

def test_refresh_token():
    # Step 1: Register a user
    register_payload = {
        "name": "Refresh_User",
        "email": "refreshuser@gmail.com",
        "password": "refreshpass1"
    }

    client.post("/api/auth/register", json=register_payload)

    # Step 2: Login to get refresh token
    login_payload = {
        "email": "refreshuser@gmail.com",
        "password": "refreshpass1"
    }

    login_response = client.post("/api/auth/login", json=login_payload)
    assert login_response.status_code == 200

    tokens = login_response.json()
    refresh_token = tokens["refresh_token"]

    # Step 3: Use refresh token to get new access token
    refresh_response = client.post("/api/auth/refresh", json={"refresh_token": refresh_token})

    assert refresh_response.status_code == 200

    data = refresh_response.json()

    # Must return new access token
    assert "access_token" in data
    assert len(data["access_token"]) > 20  # Token length sanity check

def test_get_me():
    # Step 1: Register user
    register_payload = {
        "name": "Me_User",
        "email": "meuser@gmail.com",
        "password": "mepassword1"
    }

    client.post("/api/auth/register", json=register_payload)

    # Step 2: Login to get access token
    login_payload = {
        "email": "meuser@gmail.com",
        "password": "mepassword1"
    }

    login_response = client.post("/api/auth/login", json=login_payload)
    assert login_response.status_code == 200

    tokens = login_response.json()
    access_token = tokens["access_token"]

    # Step 3: Call /me with Bearer token
    headers = {"Authorization": f"Bearer {access_token}"}
    me_response = client.get("/api/auth/me", headers=headers)

    assert me_response.status_code == 200

    user_data = me_response.json()

    # Validate user info returned
    assert user_data["email"] == "meuser@gmail.com"
    assert user_data["name"] == "Me_User"
    assert "id" in user_data

def test_forgot_and_reset_password():
    # Register a user
    payload = {
        "name": "ResetUser",
        "email": "resetuser@gmail.com",
        "password": "resetpass1"
    }
    client.post("/api/auth/register", json=payload)

    # Forgot password → get reset token
    forgot_response = client.post("/api/auth/forgot-password", json={
        "email": "resetuser@gmail.com"
    })
    assert forgot_response.status_code == 200

    reset_token = forgot_response.json()["reset_token"]
    assert reset_token is not None

    # Reset password using the token
    reset_response = client.post("/api/auth/reset-password", json={
        "token": reset_token,
        "new_password": "newpass123"
    })

    assert reset_response.status_code == 200
    assert reset_response.json()["message"] == "Password reset successful"

    # Login with new password
    login_response = client.post("/api/auth/login", json={
        "email": "resetuser@gmail.com",
        "password": "newpass123"
    })

    assert login_response.status_code == 200

