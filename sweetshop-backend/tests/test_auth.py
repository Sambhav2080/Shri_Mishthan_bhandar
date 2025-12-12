from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
def test_register_user():
    #assigning payload
    payload = {
        "name":"Sambhav",
        "email":"sambhavoct2004@gmail.com",
        "password":"password123"
    }
    #creating a post request
    response = client.post("/api/auth/register",json=payload)

    #results expected
    assert response.status_code ==201
    data = response.json()

    #return valid fields
    assert data["name"] =="Sambhav"
    assert data["email"] =="sambhavoct2004@gmail.com"
    assert "id" in data