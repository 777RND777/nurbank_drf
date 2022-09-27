import pytest


@pytest.mark.django_db
def test_register(client, user_payload):
    response = client.post("/register/", user_payload)
    assert response.status_code == 201

    data = response.data
    assert data['username'] == user_payload['username']
    assert data['first_name'] == user_payload['first_name']
    assert data['last_name'] == user_payload['last_name']
    assert "password" not in data


@pytest.mark.django_db
def test_login(client, user_payload, login_info):
    _ = client.post("/register/", user_payload)
    response = client.post("/login/", login_info)
    assert response.status_code == 200
    assert response.data.get("token") is not None


@pytest.mark.django_db
def test_user_detail(user_client, user_payload):
    response = user_client.get("/me/")
    assert response.status_code == 200

    data = response.data
    assert data['username'] == user_payload['username']
    assert data['first_name'] == user_payload['first_name']
    assert data['last_name'] == user_payload['last_name']
    assert data['debt'] == 0
    assert "password" not in data


@pytest.mark.django_db
def test_create_applications(user_client, application_payload):
    response = user_client.post("/me/applications/", application_payload)
    assert response.status_code == 201

    data = response.data
    assert data['value'] == application_payload['value']
    assert "request_date" in data
    assert len(data.keys()) == 2


@pytest.mark.django_db
def test_get_applications(user_client_with_applications, application_payload):
    response = user_client_with_applications.get("/me/applications/")
    assert response.status_code == 200

    data = response.data
    assert len(data) == 1

    application = data[0]
    assert application['value'] == application_payload['value']
    assert not application['approved']
    assert not application['answer_date']
    assert "request_date" in application
    assert len(application.keys()) == 4
