from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
# def test_register_user():
#     #assigning payload
#     payload = {
#         "name":"Sambhav",
#         "email":"sambhavoct2004@gmail.com",
#         "password":"password123"
#     }
#     #creating a post request
#     response = client.post("/api/auth/register",json=payload)

#     #results expected
#     assert response.status_code ==201
#     data = response.json()

#     #return valid fields
#     assert data["name"] =="Sambhav"
#     assert data["email"] =="sambhavoct2004@gmail.com"
#     assert "id" in data

def test_login_user():
    register_payload = {
        "name" : "Sambhav",
        "email" : "sambhavoct2004@gmail.com",
        "password" : "password123"
    }

    client.post("/api.//auth/register",json=register_payload)

    ##try a login attempt 
    login_payload = {
        "email": "sambhavoct2004@gmail.com",
        "password" : "password123"
    }

    response = client.post("/api/auth/login",json=login_payload)

    #expected results
    assert response.status_code ==200
    data = response.json()
    
    assert data["email"]=="sambhavoct2004@gmail.com"
    assert "token" in data #expected to get a token in return from login