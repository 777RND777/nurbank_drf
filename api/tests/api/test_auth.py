import pytest
from rest_framework import status


@pytest.mark.django_db
def test_register(client, user_payload):
    response = client.post("/register/", {})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response = client.post("/register/", {"username": user_payload['username']})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response = client.post("/register/", {"password": user_payload['password']})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response = client.post("/register/", {"username": user_payload['username'], "password": ""})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response = client.post("/register/", {"username": "", "password": user_payload['password']})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response = client.post("/register/", user_payload)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.data
    assert data['username'] == user_payload['username']
    assert data['first_name'] == user_payload['first_name']
    assert data['last_name'] == user_payload['last_name']
    assert len(data) == 3  # without password


@pytest.mark.django_db
def test_login(client, user_payload, login_info):
    _ = client.post("/register/", user_payload)
    response = client.post("/login/", {"username": login_info['username']})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.post("/login/", {"password": login_info['password']})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.post("/login/", {"username": "incorrect_username", "password": login_info['password']})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = client.post("/login/", login_info)
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data


@pytest.mark.django_db
def test_auth_required_url(client, user_payload):
    _ = client.post("/register/", user_payload)
    response = client.get("/me/")
    assert response.status_code == status.HTTP_403_FORBIDDEN
