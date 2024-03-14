import pytest

from django.db.utils import IntegrityError

from users.utils import generate_external_id
from users.models import User
from users.tests.factories import UserFactory


def test_generate_external_id():
    external_id = generate_external_id()
    assert isinstance(external_id, str)
    assert len(external_id) == 36


@pytest.mark.django_db
def test_external_id_is_created_after_create_an_user():
    user = UserFactory()
    assert user.external_id != ""
    assert isinstance(user.external_id, str)
    assert len(user.external_id) == 36


@pytest.mark.django_db
def test_external_id_unchanged_after_save_existing_user(user):
    external_id = user.external_id
    user.save()
    updated_user = User.objects.get(pk=user.pk)
    assert external_id == updated_user.external_id


@pytest.mark.django_db
def test_fail_when_saving_existing_external_id(user):
    with pytest.raises(IntegrityError):
        UserFactory(external_id=user.external_id)


@pytest.mark.django_db
def test_new_external_id_generated_when_existing_is_picked(user, mocker):
    mocker.patch(
        "users.utils.generate_external_id",
        side_effect=[user.external_id, generate_external_id],
        autospec=True,
    )
    new_user = UserFactory()
    assert new_user.external_id != user.external_id
