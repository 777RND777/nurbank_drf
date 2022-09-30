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
    assert "password" not in data

    response = client.post("/register/", user_payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_token(client, user_payload):
    _ = client.post("/register/", user_payload)
    response = client.post("/token/", {"username": user_payload['username']})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response = client.post("/token/", {"password": user_payload['password']})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response = client.post("/token/", {"username": "incorrect_username", "password": user_payload['password']})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.post("/token/", user_payload)
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data


@pytest.mark.django_db
def test_use_token(client, user_payload):
    _ = client.post("/register/", user_payload)
    response = client.get("/me/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    token = client.post("/token/", user_payload).data['access']
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = client.get("/me/")
    assert response.status_code == status.HTTP_200_OK
