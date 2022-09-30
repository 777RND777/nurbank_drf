import pytest
from rest_framework.test import APIClient

from bank.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def value():
    return 500


@pytest.fixture
def n():
    return 3


@pytest.fixture
def user_payload():
    return {
        "username": "test_username",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "password": "test_password",
    }


@pytest.fixture
def user_change_payload():
    return {
        "first_name": "new_first_name",
        "last_name": "new_last_name",
        "username": "new_username",
        "debt": 5000,
        "password": "new_password"
    }


@pytest.fixture
def user_client(client, user_payload):
    _ = client.post("/register/", user_payload)
    token = client.post("/token/", user_payload).data['access']
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def user_client_with_application(user_client, value):
    _ = user_client.post("/me/applications/", {"value": value})
    return user_client


@pytest.fixture
def admin_payload():
    return {
        "username": "admin",
        "password": "root",
    }


@pytest.fixture
def admin_client(user_client_with_application, admin_payload):
    _ = User.objects.create_superuser(**admin_payload)
    token = user_client_with_application.post("/token/", admin_payload).data['access']
    user_client_with_application.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return user_client_with_application


@pytest.fixture
def admin_client_users(admin_client, admin_payload, user_payload, value, n):
    for i in range(1, n):
        user_payload_current = {**user_payload, "username": f"test_user{i}"}
        User.objects.create_user(**user_payload_current)
        token = admin_client.post("/token/", user_payload_current).data['access']
        admin_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        _ = admin_client.post("/me/applications/", {"value": value})

    token = admin_client.post("/token/", admin_payload).data['access']
    admin_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return admin_client
