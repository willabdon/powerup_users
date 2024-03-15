import factory

from faker import Factory as FakerFactory


faker = FakerFactory.create()


USER_TEST_PASSWORD = "us3r_p@ss"


class UserFactory(factory.django.DjangoModelFactory):
    """User factory."""

    first_name = factory.LazyAttribute(lambda x: faker.name())
    last_name = factory.LazyAttribute(lambda x: faker.name())
    email = factory.LazyAttribute(lambda x: faker.email())
    password = factory.PostGenerationMethodCall("set_password", USER_TEST_PASSWORD)

    class Meta:
        model = "users.User"
