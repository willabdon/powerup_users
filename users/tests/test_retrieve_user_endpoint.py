import pytest

from users.models import User
from users.serializers import UserCreateRetrieveSerializer
from users.tests.factories import UserFactory


URL = "/users/{id}/"


@pytest.mark.django_db
def test_fail_user_id_or_external_id_does_not_exist(api_client, login_user):
    response = api_client.get(
        URL.format(id=0),
        content_type="application/json",
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_fail_unauthenticated_user(api_client, user):
    response = api_client.get(
        URL.format(id=user.id),
        content_type="application/json",
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_fail_retrieve_different_user_from_authenticated(api_client, login_user):
    different_user = UserFactory()
    response = api_client.get(
        URL.format(id=different_user.id),
        content_type="application/json",
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_success_request_sending_user_id(api_client, login_user):
    response = api_client.get(
        URL.format(id=login_user.id),
        content_type="application/json",
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_success_request_sending_user_external_id(api_client, login_user):
    response = api_client.get(
        URL.format(id=login_user.external_id),
        content_type="application/json",
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_response_matches_with_serializer(api_client, login_user):
    response = api_client.get(
        URL.format(id=login_user.id),
        content_type="application/json",
    )
    data = response.json()
    user = User.objects.get(id=login_user.id)
    assert data == UserCreateRetrieveSerializer(user).data
