import pytest
from rest_framework.test import APIClient

from bank.models import User


@pytest.fixture
def client():
    return APIClient()


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
def application_payload():
    return {
        "value": 5000
    }


@pytest.fixture
def admin_payload():
    return {
        "username": "admin",
        "password": "root",
    }


@pytest.fixture
def user_client(client, user_payload):
    _ = client.post("/register/", user_payload)
    _ = client.post("/login/", user_payload)
    return client


@pytest.fixture
def user_client_with_application(user_client, application_payload):
    _ = user_client.post("/me/applications/", application_payload)
    return user_client


@pytest.fixture
def admin_client_with_user(user_client_with_application, admin_payload):
    _ = User.objects.create_superuser(**admin_payload)
    _ = user_client_with_application.post("/login/", admin_payload)
    return user_client_with_application
