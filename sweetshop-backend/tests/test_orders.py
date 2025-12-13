from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ---------------- PURCHASE TEST ----------------
def test_purchase_sweet():
    # Create a new sweet
    sweet_payload = {
        "name": "Gulab Jamun",
        "category": "Dessert",
        "price": 50,
        "quantity": 10
    }
    create_res = client.post("/api/sweets", json=sweet_payload)
    sweet_id = create_res.json()["id"]

    # Purchase 3 units
    purchase_res = client.post(f"/api/sweets/{sweet_id}/purchase", json={"quantity": 3})
    assert purchase_res.status_code == 200
    assert purchase_res.json()["remaining_quantity"] == 7


# ---------------- OUT OF STOCK TEST ----------------
def test_purchase_out_of_stock():
    sweet_payload = {
        "name": "Ladoo",
        "category": "Dessert",
        "price": 30,
        "quantity": 1
    }
    create_res = client.post("/api/sweets", json=sweet_payload)
    sweet_id = create_res.json()["id"]

    # Try to purchase more than available
    purchase_res = client.post(f"/api/sweets/{sweet_id}/purchase", json={"quantity": 5})
    assert purchase_res.status_code == 400


# ---------------- RESTOCK (ADMIN ONLY) ----------------
def test_restock_admin_only():
    # Create sweet
    sweet_payload = {
        "name": "Barfi",
        "category": "Dessert",
        "price": 40,
        "quantity": 5
    }
    create_res = client.post("/api/sweets", json=sweet_payload)
    sweet_id = create_res.json()["id"]

    # Register admin
    admin_payload = {
        "name": "Admin",
        "email": "admin123@gmail.com",
        "password": "adminpass1"
    }
    client.post("/api/auth/register", json=admin_payload)

    # Login admin
    login_res = client.post("/api/auth/login", json={
        "email": "admin123@gmail.com",
        "password": "adminpass1"
    })
    admin_token = login_res.json()["access_token"]

    # Restock using admin token
    restock_res = client.post(
        f"/api/sweets/{sweet_id}/restock",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"quantity": 10}
    )

    assert restock_res.status_code == 200
    assert restock_res.json()["new_quantity"] == 15


# ---------------- CART CHECKOUT ----------------
def test_cart_checkout():
    sweet_payload = {
        "name": "Jalebi",
        "category": "Dessert",
        "price": 25,
        "quantity": 20
    }
    create_res = client.post("/api/sweets", json=sweet_payload)
    sweet_id = create_res.json()["id"]

    # Add to cart
    cart_add_res = client.post("/api/cart/add", json={"sweet_id": sweet_id, "quantity": 5})
    assert cart_add_res.status_code == 200

    # Checkout
    checkout_res = client.post("/api/cart/checkout")
    assert checkout_res.status_code == 200
    assert checkout_res.json()["message"] == "Order placed successfully"
