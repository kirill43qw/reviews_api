import pytest

from core.apps.common.containers import get_container
from core.apps.reviews.entities.comments import CommentEntity
from core.apps.reviews.services.comments import BaseCommentService, ORMCommentService
from core.apps.reviews.services.reviews import BaseReviewValidatorService
from core.apps.reviews.use_cases.comment_crud import (
    CreateCommentUseCase,
    DeleteCommentUseCase,
    UpdateCommentUseCase,
)
from core.apps.reviews.use_cases.review_dto import CreateReviewUseCase
from tests.factories import AuthorModelFactory, CommentModelFactory, ReviewModelFactory
from tests.factories.title import TitleModelFactory


@pytest.fixture
def container():
    return get_container()


@pytest.fixture
def comment_service() -> BaseCommentService:
    return ORMCommentService()


@pytest.fixture
def review_validator(container):
    """fixture for review_validators"""
    return container.resolve(BaseReviewValidatorService)


@pytest.fixture
def create_review_use_case(container):
    return container.resolve(CreateReviewUseCase)


@pytest.fixture
def create_comment_use_case(container):
    return container.resolve(CreateCommentUseCase)


@pytest.fixture
def update_comment_use_case(container):
    return container.resolve(UpdateCommentUseCase)


@pytest.fixture
def delete_comment_use_case(container):
    return container.resolve(DeleteCommentUseCase)


@pytest.fixture
def user():
    return AuthorModelFactory(role="user")


@pytest.fixture
def moderator():
    return AuthorModelFactory(role="moderator")


@pytest.fixture
def admin():
    return AuthorModelFactory(role="admin")


@pytest.fixture
def review():
    return ReviewModelFactory()


@pytest.fixture
def title():
    return TitleModelFactory()


@pytest.fixture
def comment(user):
    return CommentModelFactory(author=user)


@pytest.fixture
def comment_data():
    return CommentEntity(text="check_comment")
