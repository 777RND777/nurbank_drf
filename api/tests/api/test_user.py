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
def test_create_application(user_client, value):
    response = user_client.post("/me/applications/", {})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response = user_client.post("/me/applications/", {"value": value})
    assert response.status_code == status.HTTP_201_CREATED

    data = response.data
    assert data['value'] == value
    assert "request_date" in data
    # TODO add creating new application with failure
    #  because there can be only one active application for each user


@pytest.mark.django_db
def test_get_application_list(user_client_with_application, value):
    response = user_client_with_application.get("/me/applications/")
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    assert len(data) == 1

    application = data[0]
    assert application['value'] == value
    assert not application['approved']
    assert not application['answer_date']
    assert "request_date" in application
