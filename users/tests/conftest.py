import pytest

from users.tests.factories import UserFactory


@pytest.fixture
def user():
    return UserFactory()
