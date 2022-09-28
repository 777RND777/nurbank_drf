import pytest
from rest_framework import status


@pytest.mark.django_db
def test_get_user_list(admin_client_with_user):
    response = admin_client_with_user.get("/users/")
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    assert len(data) == 2
