import json
import pytest

from django.utils import timezone

from users.models import User
from users.serializers import UserUpdateSerializer
from users.tests.factories import UserFactory


URL = "/users/{id}/"


@pytest.fixture
def user_update_request_data():
    return {
        "first_name": "Alice",
        "last_name": "Bob",
    }


@pytest.mark.django_db
def test_fail_user_id_or_external_id_does_not_exist(
    api_client, user_update_request_data, login_user
):
    response = api_client.put(
        URL.format(id=0),
        data=json.dumps(user_update_request_data),
        content_type="application/json",
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_fail_unauthenticated_user(api_client, user_update_request_data, user):
    response = api_client.put(
        URL.format(id=user.id),
        data=json.dumps(user_update_request_data),
        content_type="application/json",
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_fail_update_different_user_from_authenticated(
    api_client, user_update_request_data, login_user
):
    different_user = UserFactory()
    response = api_client.put(
        URL.format(id=different_user.id),
        data=json.dumps(user_update_request_data),
        content_type="application/json",
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_success_request_sending_user_id(
    api_client, user_update_request_data, login_user
):
    response = api_client.put(
        URL.format(id=login_user.id),
        data=json.dumps(user_update_request_data),
        content_type="application/json",
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_success_request_sending_user_external_id(
    api_client, user_update_request_data, login_user
):
    response = api_client.put(
        URL.format(id=login_user.external_id),
        data=json.dumps(user_update_request_data),
        content_type="application/json",
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_updated_at_was_updated(api_client, user_update_request_data, login_user):
    api_client.put(
        URL.format(id=login_user.id),
        data=json.dumps(user_update_request_data),
        content_type="application/json",
    )
    user = User.objects.get(id=login_user.id)
    assert user.updated_at == timezone.now().date()


@pytest.mark.django_db
def test_response_matches_with_serializer(
    api_client, user_update_request_data, login_user
):
    response = api_client.put(
        URL.format(id=login_user.id),
        data=json.dumps(user_update_request_data),
        content_type="application/json",
    )
    data = response.json()
    user = User.objects.get(id=login_user.id)
    assert data == UserUpdateSerializer(user).data
