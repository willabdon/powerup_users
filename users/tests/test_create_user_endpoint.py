import json
import pytest

from django.utils import timezone

from users.models import User
from users.serializers import UserCreateSerializer


URL = "/users/"


@pytest.fixture
def user_create_request_data():
    return {
        "first_name": "Alice",
        "last_name": "Bob",
        "email": "alicebob@email.com",
        "password": "s0m3Str0ngp@ssw0rd",
        "confirm_password": "s0m3Str0ngp@ssw0rd",
    }


@pytest.mark.django_db
def test_success_request(api_client, user_create_request_data):
    response = api_client.post(
        URL, data=json.dumps(user_create_request_data), content_type="application/json"
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_user_is_sucessfuly_created(api_client, user_create_request_data):
    api_client.post(
        URL, data=json.dumps(user_create_request_data), content_type="application/json"
    )
    assert User.objects.filter(email=user_create_request_data["email"]).exists()


@pytest.mark.django_db
def test_user_created_date_exists(api_client, user_create_request_data):
    api_client.post(
        URL, data=json.dumps(user_create_request_data), content_type="application/json"
    )
    user = User.objects.get(email=user_create_request_data["email"])
    assert user.created_date == timezone.now().date()


@pytest.mark.django_db
def test_user_external_id_exists(api_client, user_create_request_data):
    api_client.post(
        URL, data=json.dumps(user_create_request_data), content_type="application/json"
    )
    user = User.objects.get(email=user_create_request_data["email"])
    assert user.external_id != ""
    assert isinstance(user.external_id, str)
    assert len(user.external_id) == 36


@pytest.mark.django_db
def test_response_matches_with_serializer(api_client, user_create_request_data):
    response = api_client.post(
        URL, data=json.dumps(user_create_request_data), content_type="application/json"
    )
    data = response.json()
    user = User.objects.get(email=user_create_request_data["email"])
    assert data == UserCreateSerializer(user).data


@pytest.mark.django_db
def test_password_is_not_saved_as_plain_text(api_client, user_create_request_data):
    api_client.post(
        URL, data=json.dumps(user_create_request_data), content_type="application/json"
    )
    user = User.objects.get(email=user_create_request_data["email"])
    assert user.password != user_create_request_data["password"]


# TODO


@pytest.mark.django_db
def test_request_fail_if_password_dont_match(api_client, user_create_request_data):
    user_create_request_data["confirm_password"] = "dummyvalue"
    response = api_client.post(
        URL, data=json.dumps(user_create_request_data), content_type="application/json"
    )
    data = response.json()
    assert response.status_code == 400
    assert data["password"] == ["Password fields didn't match."]


@pytest.mark.django_db
def test_request_fail_if_email_already_registered(
    api_client, user_create_request_data, user
):
    user_create_request_data["email"] = user.email
    response = api_client.post(
        URL, data=json.dumps(user_create_request_data), content_type="application/json"
    )
    data = response.json()
    assert response.status_code == 400
    assert data["email"] == ["user with this email address already exists."]


@pytest.mark.django_db
def test_request_fail_if_password_is_numeric(api_client, user_create_request_data):
    user_create_request_data["password"] = "123456789"
    user_create_request_data["confirm_password"] = "123456789"
    response = api_client.post(
        URL, data=json.dumps(user_create_request_data), content_type="application/json"
    )
    data = response.json()
    assert response.status_code == 400
    assert data["password"] == ["This password is entirely numeric."]


@pytest.mark.django_db
def test_request_fail_if_password_length_less_then_8(
    api_client, user_create_request_data
):
    user_create_request_data["password"] = "12ABcd*"
    user_create_request_data["confirm_password"] = "12ABcd*"
    response = api_client.post(
        URL, data=json.dumps(user_create_request_data), content_type="application/json"
    )
    data = response.json()
    assert response.status_code == 400
    assert data["password"] == [
        "This password is too short. It must contain at least 8 characters."
    ]
