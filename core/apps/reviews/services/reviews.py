from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.apps.customers.entities import CustomerEntity
from core.apps.reviews.entities import TitleEntity, ReviewEntity
from core.apps.reviews.exceptions.reviews import ReviewInvalidRating
from core.apps.reviews.models import Review as ReviewDTO


class BaseReviewService(ABC):
    # @abstractmethod
    # def check_review_exists(
    #     self, title: TitleEntity, author: CustomerEntity
    # ) -> bool: ...

    @abstractmethod
    def save_review(
        self, title: TitleEntity, author: CustomerEntity, review: ReviewEntity
    ) -> ReviewEntity: ...


class ORMReviewService(BaseReviewService):
    def save_review(
        self, title: TitleEntity, author: CustomerEntity, review: ReviewEntity
    ) -> ReviewEntity:
        review_dto = ReviewDTO.from_entity(review=review, title=title, customer=author)
        review_dto.save()
        return review_dto.to_entity()


class BaseReviewValidatorService(ABC):
    def validate(
        self,
        review: ReviewEntity,
        customer: CustomerEntity | None = None,
        title: TitleEntity | None = None,
    ): ...


class ReviewRatingValidatorService(BaseReviewValidatorService):
    def validate(self, review: ReviewEntity, *args, **kwargs):
        if not (1 <= review.rating <= 10):
            raise ReviewInvalidRating(rating=review.rating)


@dataclass
class ComposedReviewValidatorService(BaseReviewValidatorService):
    validators: list[BaseReviewValidatorService]

    def validate(
        self,
        review: ReviewEntity,
        customer: CustomerEntity | None = None,
        title: TitleEntity | None = None,
    ):
        for validator in self.validators:
            validator.validate(review=review, customer=customer, title=title)
