import factory
from factory.django import DjangoModelFactory
from core.apps.reviews.models import Title
from tests.factories.category import CategoryModelFactory


class TitleModelFactory(DjangoModelFactory):
    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph")
    year = factory.Faker("year")
    category = factory.SubFactory(CategoryModelFactory)

    @factory.post_generation
    def genre(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.genre.set(extracted)

    class Meta:
        model = Title
