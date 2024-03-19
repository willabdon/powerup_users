import pytest

from users.tests.factories import UserFactory


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def login_user(api_client, user):
    api_client.force_authenticate(user=user)
    return user
