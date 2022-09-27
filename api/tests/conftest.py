import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_client(client, user_payload):
    _ = client.post("/register/", user_payload)
    _ = client.post("/login/", user_payload)
    return client


@pytest.fixture
def user_client_with_applications(user_client, application_payload):
    _ = user_client.post("/me/applications/", application_payload)
    return user_client


@pytest.fixture
def user_payload():
    return {
        "username": "test_username",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "password": "test_password",
    }


@pytest.fixture
def application_payload():
    return {
        "value": 5000
    }
