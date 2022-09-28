import pytest
from rest_framework import status


@pytest.mark.django_db
def test_get_user_list(admin_client_with_user):
    response = admin_client_with_user.get("/users/")
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    assert len(data) == 2


@pytest.mark.django_db
def test_get_user(admin_client_with_user, user_payload):
    response = admin_client_with_user.get(f"/users/unregistered_user/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = admin_client_with_user.get(f"/users/{user_payload['username']}/")
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    for key in user_payload:
        assert key in data
    assert data['password'] != user_payload['password']


@pytest.mark.django_db
def test_patch_user(client, admin_client_with_user, user_payload, user_change_payload):
    response = admin_client_with_user.patch(f"/users/unregistered_user/", user_change_payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = admin_client_with_user.patch(f"/users/{user_payload['username']}/", user_change_payload)
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    assert data['first_name'] == user_change_payload['first_name']
    assert data['last_name'] == user_change_payload['last_name']
    assert data['debt'] == user_change_payload['debt']
    assert data['username'] == user_payload['username']
    # TODO create your own UserManager
    #  password does not change. So test should be working,
    #  but method .save() in User model hashes password again...
    # assert admin_client_with_user.post("/login/", user_payload).status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_delete_user(admin_client_with_user, user_payload):
    response = admin_client_with_user.delete(f"/users/unregistered_user/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = admin_client_with_user.delete(f"/users/{user_payload['username']}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = admin_client_with_user.get(f"/users/{user_payload['username']}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
