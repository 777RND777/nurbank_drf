import pytest
from rest_framework import status


@pytest.mark.django_db
def test_get_user_list(admin_client, n):
    response = admin_client.get("/users/")
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    assert len(data) == 1


@pytest.mark.django_db
def test_get_user(admin_client_full, admin_user_payload):
    response = admin_client_full.get(f"/users/unregistered_user/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = admin_client_full.get(f"/users/{admin_user_payload['username']}/")
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    for key in admin_user_payload:
        assert key in data
    assert data['password'] != admin_user_payload['password']


@pytest.mark.django_db
def test_patch_user(admin_client_full, admin_user_payload, user_change_payload):
    response = admin_client_full.patch(f"/users/unregistered_user/", user_change_payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = admin_client_full.patch(f"/users/{admin_user_payload['username']}/", user_change_payload)
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    assert data['first_name'] == user_change_payload['first_name']
    assert data['last_name'] == user_change_payload['last_name']
    assert data['debt'] == user_change_payload['debt']
    assert data['username'] == f"{admin_user_payload['username']}"

    response = admin_client_full.post("/login/", admin_user_payload)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_delete_user(admin_client_full, admin_user_payload):
    response = admin_client_full.delete(f"/users/unregistered_user/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = admin_client_full.delete(f"/users/{admin_user_payload['username']}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = admin_client_full.get(f"/users/{admin_user_payload['username']}/")
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
