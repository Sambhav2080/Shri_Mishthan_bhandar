from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ---------- Helper: Create admin + login ----------
def create_admin_and_login():
    admin_payload = {
        "name": "AdminUser",
        "email": "adminproduct@gmail.com",
        "password": "adminpass1",
        "role": "admin"
    }
    client.post("/api/auth/register", json=admin_payload)

    login_response = client.post("/api/auth/login", json={
        "email": "adminproduct@gmail.com",
        "password": "adminpass1"
    })
    data = login_response.json()
    return data["access_token"]

# -------------------- TEST 1: Create product (admin only) --------------------
def test_create_product():
    token = create_admin_and_login()

    response = client.post("/api/sweets", 
        json={
            "name": "Gulab Jamun",
            "price": 120,
            "category": "Sweets",
            "stock": 50
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Gulab Jamun"
    assert data["price"] == 120


# -------------------- TEST 2: Normal user cannot create product --------------------
def test_user_cannot_create_product():
    # Create normal user
    payload = {
        "name": "NormalUser",
        "email": "normaluser@gmail.com",
        "password": "normalpass1"
    }
    client.post("/api/auth/register", json=payload)

    login_response = client.post("/api/auth/login", json={
        "email": "normaluser@gmail.com",
        "password": "normalpass1"
    })

    token = login_response.json()["access_token"]

    response = client.post("/api/sweets",
        json={
            "name": "Barfi",
            "price": 200,
            "category": "Sweets",
            "stock": 20
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403  # Forbidden

# -------------------- TEST 3: Get all products --------------------
def test_get_all_products():
    response = client.get("/api/sweets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# -------------------- TEST 4: Update product (admin only) --------------------
def test_update_product():
    token = create_admin_and_login()

    # Create product
    create_res = client.post("/api/sweets",
        json={
            "name": "Rasgulla",
            "price": 150,
            "category": "Sweets",
            "stock": 30
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    product_id = create_res.json()["id"]
    # Update
    update_res = client.put(f"/api/sweets/{product_id}",
        json={"price": 180},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert update_res.status_code == 200
    assert update_res.json()["price"] == 180

# -------------------- TEST 5: Delete product (admin only) --------------------
def test_delete_product():
    token = create_admin_and_login()
    # Create product
    create_res = client.post("/api/sweets",
        json={
            "name": "Ladoo",
            "price": 100,
            "category": "Sweets",
            "stock": 40
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    product_id = create_res.json()["id"]
    delete_res = client.delete(f"/api/sweets/{product_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Product deleted successfully"
