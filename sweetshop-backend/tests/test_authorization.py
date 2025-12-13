from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ------------------ ROLE ASSIGNMENT TEST ------------------

def test_role_assignment():
    payload = {
        "name": "RoleUser",
        "email": "roleuser@gmail.com",
        "password": "userpass1"
    }

    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 201
    
    data = res.json()
    assert data["role"] == "user"   # default role


# ------------------ USER BLOCKED FROM ADMIN ROUTE ------------------

def test_admin_access_denied_for_user():
    # Register normal user
    payload = {
        "name": "NormalUser",
        "email": "normal@gmail.com",
        "password": "normalpass1"
    }
    client.post("/api/auth/register", json=payload)

    # Login
    login_res = client.post("/api/auth/login", json={
        "email": "normal@gmail.com",
        "password": "normalpass1"
    })
    token = login_res.json()["access_token"]

    # Try accessing admin route
    res = client.get(
        "/api/auth/admin-only",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert res.status_code == 403
    assert res.json()["detail"] == "Admin access required"


# ------------------ ADMIN CAN ACCESS ADMIN ROUTE ------------------

def test_admin_can_access():
    # Register admin
    payload = {
        "name": "AdminUser",
        "email": "admin@gmail.com",
        "password": "adminpass1",
        "role": "admin"
    }
    client.post("/api/auth/register", json=payload)

    # Login
    login_res = client.post("/api/auth/login", json={
        "email": "admin@gmail.com",
        "password": "adminpass1"
    })
    token = login_res.json()["access_token"]

    # Hit admin route
    res = client.get(
        "/api/auth/admin-only",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 200
    assert res.json()["message"] == "Welcome Admin"
