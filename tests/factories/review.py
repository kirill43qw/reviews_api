import factory
from factory.django import DjangoModelFactory

from core.apps.reviews.models import Review
from tests.factories import AuthorModelFactory, TitleModelFactory


class ReviewModelFactory(DjangoModelFactory):
    author = factory.SubFactory(AuthorModelFactory)
    title = factory.SubFactory(TitleModelFactory)
    rating = factory.Faker("random_int", min=1, max=10)
    text = factory.Faker("paragraph", nb_sentences=3)

    class Meta:
        model = Review
