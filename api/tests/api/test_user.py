import pytest
from rest_framework import status


@pytest.mark.django_db
def test_get_user(user_client, user_payload):
    response = user_client.get("/me/")
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    assert data['username'] == user_payload['username']
    assert data['first_name'] == user_payload['first_name']
    assert data['last_name'] == user_payload['last_name']
    assert data['debt'] == 0


@pytest.mark.django_db
def test_update_user(user_client, user_payload, user_change_payload):
    response = user_client.patch("/me/", user_change_payload)
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    assert data['first_name'] == user_change_payload['first_name']
    assert data['last_name'] == user_change_payload['last_name']
    assert data['username'] == user_payload['username']
    assert data['debt'] == 0
    assert "password" not in data


@pytest.mark.django_db
def test_create_applications(user_client, application_payload):
    response = user_client.post("/me/applications/", application_payload)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.data
    assert data['value'] == application_payload['value']
    assert "request_date" in data


@pytest.mark.django_db
def test_get_applications(user_client_with_application, application_payload):
    response = user_client_with_application.get("/me/applications/")
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    assert len(data) == 1

    application = data[0]
    assert application['value'] == application_payload['value']
    assert not application['approved']
    assert not application['answer_date']
    assert "request_date" in application
