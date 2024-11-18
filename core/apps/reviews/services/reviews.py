from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime

from core.api.filters import PaginationIn
from core.apps.customers.entities import CustomerEntity
from core.apps.reviews.entities import TitleEntity, ReviewEntity
from core.apps.reviews.exceptions.reviews import (
    ReviewInvalidRating,
    ReviewNotFount,
    SingleReviewError,
)
from core.apps.reviews.models import Review as ReviewDTO


class BaseReviewService(ABC):
    @abstractmethod
    def get_review_list(
        self, title_id: int, pagination: PaginationIn
    ) -> Iterable[ReviewEntity]: ...

    @abstractmethod
    def get_by_id(self, review_id: int) -> ReviewDTO: ...

    @abstractmethod
    def check_review_exists(
        self, title: TitleEntity, author: CustomerEntity
    ) -> bool: ...

    @abstractmethod
    def save_review(
        self, title: TitleEntity, author: CustomerEntity, review: ReviewEntity
    ) -> ReviewEntity: ...

    @abstractmethod
    def update_review(
        self, review: ReviewDTO, review_data=ReviewEntity
    ) -> ReviewEntity: ...

    @abstractmethod
    def delete_review(self, review: ReviewDTO) -> None: ...


class ORMReviewService(BaseReviewService):
    def get_review_list(
        self, title_id: int, pagination: PaginationIn
    ) -> Iterable[ReviewEntity]:
        query = ReviewDTO.objects.filter(title_id=title_id)[
            pagination.offset : pagination.offset + pagination.limit
        ]
        return [review.to_entity() for review in query]

    def get_by_id(self, review_id: int) -> ReviewDTO:
        try:
            return ReviewDTO.objects.select_related("author", "title").get(id=review_id)
        except ReviewDTO.DoesNotExist:
            raise ReviewNotFount(review_id=review_id)

    def check_review_exists(self, title: TitleEntity, author: CustomerEntity) -> bool:
        return ReviewDTO.objects.filter(title_id=title.id, author_id=author.id).exists()

    def save_review(
        self, title: TitleEntity, author: CustomerEntity, review: ReviewEntity
    ) -> ReviewEntity:
        review_dto = ReviewDTO.from_entity(review=review, title=title, customer=author)
        review_dto.save()
        return review_dto.to_entity()

    def update_review(
        self, review: ReviewDTO, review_data=ReviewEntity
    ) -> ReviewEntity:
        fields_to_update = {
            "text": review_data.text,
            "rating": review_data.rating,
        }

        for field, value in fields_to_update.items():
            if value is not None:
                setattr(review, field, value)

        review.updated_at = datetime.now()
        review.save()

        return review.to_entity()

    def delete_review(self, review: ReviewDTO) -> None:
        review.delete()


class BaseReviewValidatorService(ABC):
    def validate(
        self,
        review: ReviewEntity,
        author: CustomerEntity | None = None,
        title: TitleEntity | None = None,
    ): ...


class ReviewRatingValidatorService(BaseReviewValidatorService):
    def validate(self, review: ReviewEntity, *args, **kwargs):
        if not (1 <= review.rating <= 10):
            raise ReviewInvalidRating(rating=review.rating)


@dataclass
class SingleReviewValidatorService(BaseReviewValidatorService):
    service: BaseReviewService

    def validate(self, author: CustomerEntity, title: TitleEntity, *args, **kwargs):
        if self.service.check_review_exists(title=title, author=author):
            # попробовать без параметров
            raise SingleReviewError(title_id=title.id, author_id=author.id)
            # raise SingleReviewError()


@dataclass
class ComposedReviewValidatorService(BaseReviewValidatorService):
    validators: list[BaseReviewValidatorService]

    def validate(
        self,
        review: ReviewEntity,
        author: CustomerEntity | None = None,
        title: TitleEntity | None = None,
    ):
        for validator in self.validators:
            validator.validate(review=review, author=author, title=title)
