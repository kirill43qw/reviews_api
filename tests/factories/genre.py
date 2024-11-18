import factory
from factory.django import DjangoModelFactory

from core.apps.reviews.models import Genre


class GenreModelFactory(DjangoModelFactory):
    title = factory.Faker("lexify", text="?????")
    slug = factory.LazyAttribute(lambda obj: obj.title.lower())

    class Meta:
        model = Genre
