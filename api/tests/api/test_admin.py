import pytest
from django.conf import settings
from rest_framework import status

from bank.models import User


@pytest.mark.django_db
def test_admin_url(user_client):
    response = user_client.get("/users/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_application(admin_client, value):
    user_id = User.objects.get(is_superuser=False).id

    response = admin_client.post("/applications/", {})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response = admin_client.post("/applications/", {"value": value})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response = admin_client.post("/applications/", {"user": user_id})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response = admin_client.post("/applications/", {"value": 0, "user": user_id})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response = admin_client.post("/applications/", {"value": -value, "user": user_id})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response = admin_client.post("/applications/", {"value": settings.MAX_APPLICATION_VALUE + 1, "user": user_id})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response = admin_client.post("/applications/", {"value": value, "user": 0})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response = admin_client.post("/applications/", {"value": value, "user": user_id})
    assert response.status_code == status.HTTP_201_CREATED

    data = response.data
    assert data['value'] == value
    assert data['user'] == user_id
    assert data['approved']
    assert data['is_admin']
    assert value == User.objects.get(is_superuser=False).debt


@pytest.mark.django_db
def test_get_application_list(admin_client_users, admin_payload, user_payload, value, n):
    response = admin_client_users.get("/applications/")
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    assert len(data) == n

    _ = admin_client_users.post("/login/", user_payload)
    _ = admin_client_users.post("/me/applications/", {"value": value})
    _ = admin_client_users.post("/login/", admin_payload)

    response = admin_client_users.get("/applications/")
    assert len(response.data) == n + 1


@pytest.mark.django_db
def test_get_active_application_list(admin_client_users, n):
    response = admin_client_users.get("/applications/active/")
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    assert len(data) == n - 1

    _ = admin_client_users.post(f"/applications/{n}/decline/")

    response = admin_client_users.get("/applications/active/")
    assert len(response.data) == n - 2


@pytest.mark.django_db
def test_get_application(admin_client, value):
    response = admin_client.get("/applications/100/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = admin_client.get("/applications/1/")
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    assert data['user'] == User.objects.get(is_superuser=False).id
    assert data['value'] == value


@pytest.mark.django_db
def test_delete_application(admin_client):
    response = admin_client.delete("/applications/100/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = admin_client.delete("/applications/1/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = admin_client.get("/applications/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_approve_application(admin_client):
    response = admin_client.post("/applications/100/approve/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = admin_client.post("/applications/1/approve/")
    assert response.status_code == status.HTTP_200_OK

    user = User.objects.get(is_superuser=False)
    data = response.data
    assert data['answer_date']
    assert data['approved']
    assert not data['is_admin']
    assert data['value'] == user.debt

    response = admin_client.post("/applications/1/approve/")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_decline_application(admin_client):
    response = admin_client.post("/applications/100/decline/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = admin_client.post("/applications/1/decline/")
    assert response.status_code == status.HTTP_200_OK

    user = User.objects.get(is_superuser=False)
    data = response.data
    assert data['answer_date']
    assert not data['approved']
    assert not data['is_admin']
    assert user.debt == 0

    response = admin_client.post("/applications/1/decline/")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_user_list(admin_client):
    response = admin_client.get("/users/")
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    assert len(data) == 2


@pytest.mark.django_db
def test_get_user(admin_client, user_payload):
    response = admin_client.get(f"/users/unregistered_user/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = admin_client.get(f"/users/{user_payload['username']}/")
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    for key in user_payload:
        assert key in data
    assert data['password'] != user_payload['password']


@pytest.mark.django_db
def test_patch_user(admin_client, user_payload, user_change_payload):
    response = admin_client.patch(f"/users/unregistered_user/", user_change_payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = admin_client.patch(f"/users/{user_payload['username']}/", user_change_payload)
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    assert data['first_name'] == user_change_payload['first_name']
    assert data['last_name'] == user_change_payload['last_name']
    assert data['debt'] == user_change_payload['debt']
    assert data['username'] == f"{user_payload['username']}"

    response = admin_client.post("/login/", user_payload)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_delete_user(admin_client, user_payload):
    response = admin_client.delete(f"/users/unregistered_user/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = admin_client.delete(f"/users/{user_payload['username']}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = admin_client.get(f"/users/{user_payload['username']}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_user_application_list(admin_client, user_payload, value):
    response = admin_client.get(f"/users/unregistered_user/applications/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = admin_client.get(f"/users/{user_payload['username']}/applications/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1

    user_id = User.objects.get(is_superuser=False).id
    _ = admin_client.post("/applications/", {"value": value, "user": user_id})

    response = admin_client.get(f"/users/{user_payload['username']}/applications/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_get_user_active_application(admin_client, user_payload):
    response = admin_client.get(f"/users/unregistered_user/active/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = admin_client.get(f"/users/{user_payload['username']}/active/")
    assert response.status_code == status.HTTP_200_OK

    _ = admin_client.delete(f"/applications/1/")

    response = admin_client.get(f"/users/{user_payload['username']}/active/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
