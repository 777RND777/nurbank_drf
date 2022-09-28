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


@pytest.mark.django_db
def test_login(client, user_payload):
    _ = client.post("/register/", user_payload)
    response = client.post("/login/", {"username": user_payload['username']})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.post("/login/", {"password": user_payload['password']})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.post("/login/", {"username": "incorrect_username", "password": user_payload['password']})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = client.post("/login/", user_payload)
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data


@pytest.mark.django_db
def test_auth_required_url(client, user_payload):
    _ = client.post("/register/", user_payload)
    response = client.get("/me/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


# TODO fix token problem
# @pytest.mark.django_db
# def test_token(user_client, client, user_payload):
#     response = user_client.post("/login/", user_payload)
#     token = response.data['token']
#
#     from rest_framework.test import APIClient
#     new_client = APIClient()
#     response = new_client.get("/me/")
#     assert response.status_code == status.HTTP_403_FORBIDDEN
#     response = new_client.get("/me/", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == status.HTTP_200_OK
