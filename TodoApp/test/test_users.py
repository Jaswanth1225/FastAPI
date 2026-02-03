from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == "sai"
    assert response.json()['email'] == "sai@example.com"
    assert response.json()['role'] == "admin"
    assert response.json()['first_name'] == "Sai"
    assert response.json()['last_name'] == "Jaswanth"
    assert response.json()['phone_number'] == "1234567890"

def test_change_password_success(test_user):
    request_data = {
        "password": "password123",
        "new_password": "newpassword456"
    }
    response = client.put("/user/user", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
   

def test_change_password_invalid_current_password(test_user):
    request_data = {
        "password": "wrongpassword",
        "new_password": "newpassword456"
    }
    response = client.put("/user/user", json=request_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        'detail': 'Incorrect password'
    }

def test_change_phone_number(test_user):
    response = client.put("/user/update_phone_number", params={"phone_number": "0987654321"})

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.id == 1).first()
    assert model.phone_number == "0987654321"