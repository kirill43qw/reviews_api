import factory
from uuid import uuid4
from faker import Faker
from factory.django import DjangoModelFactory

from core.apps.customers.models import Customer

fake = Faker()


class AuthorModelFactory(DjangoModelFactory):
    username = factory.LazyFunction(lambda: fake.user_name()[:19])
    phone = factory.LazyFunction(lambda: fake.phone_number()[:19])
    token = factory.LazyFunction(lambda: str(uuid4()))
    bio = factory.Faker("text", max_nb_chars=100)

    role = factory.Faker(
        "random_element", elements=[Customer.ADMIN, Customer.MODERATOR, Customer.USER]
    )

    class Meta:
        model = Customer
