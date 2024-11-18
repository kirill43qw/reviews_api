import factory
from factory.django import DjangoModelFactory

from core.apps.reviews.models import Comment
from tests.factories import AuthorModelFactory, ReviewModelFactory


class CommentModelFactory(DjangoModelFactory):
    review = factory.SubFactory(ReviewModelFactory)
    text = factory.Faker("paragraph", nb_sentences=3)
    author = factory.SubFactory(AuthorModelFactory)

    class Meta:
        model = Comment
