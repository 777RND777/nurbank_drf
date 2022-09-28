import pytest
from rest_framework import status


@pytest.mark.django_db
def test_admin_url(user_client):
    response = user_client.get("/users/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


# @pytest.mark.django_db
# def test_create_application(admin_client_with_one_user):
#     response = admin_client_with_one_user.post("/applications/")
#     assert response.status_code == status.HTTP_200_OK
#
#     data = response.data
#     assert len(data) == 0  # TODO
#
#
# @pytest.mark.django_db
# def test_get_application_list(admin_client_with_n_users, n):
#     response = admin_client_with_n_users.get("/applications/")
#     assert response.status_code == status.HTTP_200_OK
#
#     data = response.data
#     assert len(data) == 0  # TODO


@pytest.mark.django_db
def test_get_user_list(admin_client_with_n_users, n):
    response = admin_client_with_n_users.get("/users/")
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    assert len(data) == n + 1


@pytest.mark.django_db
def test_get_user(admin_client_with_one_user, user_payload):
    response = admin_client_with_one_user.get(f"/users/unregistered_user/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = admin_client_with_one_user.get(f"/users/{user_payload['username']}/")
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    for key in user_payload:
        assert key in data
    assert data['password'] != user_payload['password']


@pytest.mark.django_db
def test_patch_user(admin_client_with_one_user, user_payload, user_change_payload):
    response = admin_client_with_one_user.patch(f"/users/unregistered_user/", user_change_payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = admin_client_with_one_user.patch(f"/users/{user_payload['username']}/", user_change_payload)
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    assert data['first_name'] == user_change_payload['first_name']
    assert data['last_name'] == user_change_payload['last_name']
    assert data['debt'] == user_change_payload['debt']
    assert data['username'] == f"{user_payload['username']}"

    response = admin_client_with_one_user.post("/login/", user_payload)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_delete_user(admin_client_with_one_user, user_payload):
    response = admin_client_with_one_user.delete(f"/users/unregistered_user/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = admin_client_with_one_user.delete(f"/users/{user_payload['username']}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = admin_client_with_one_user.get(f"/users/{user_payload['username']}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


# @pytest.mark.django_db
# def test_get_user_application_list(admin_client_full, admin_user_payload):
#     response = admin_client_full.get(f"/users/unregistered_user/applications/")
#     assert response.status_code == status.HTTP_404_NOT_FOUND
#
#     response = admin_client_full.get(f"/users/{admin_user_payload['username']}/applications/")
#     assert response.status_code == status.HTTP_200_OK
#
#     data = response.data
#     assert len(data) == 0
