from dataclasses import dataclass

from core.apps.customers.services.customers import BaseCustomersService
from core.apps.reviews.services.reviews import (
    BaseReviewService,
    BaseReviewValidatorService,
)
from core.apps.reviews.services.titles import BaseTitleService
from core.apps.reviews.entities import ReviewEntity


@dataclass
class CreateReviewUseCase:
    review_service: BaseReviewService
    customer_service: BaseCustomersService
    title_service: BaseTitleService
    validator_service: BaseReviewValidatorService

    def execute(
        self,
        customer_token: str,
        title_id: int,
        review: ReviewEntity,
    ) -> ReviewEntity:
        author = self.customer_service.get_by_token(token=customer_token)
        title = self.title_service.get_by_id(title_id=title_id)

        self.validator_service.validate(review=review, author=author, title=title)
        saved_review = self.review_service.save_review(
            title=title, author=author, review=review
        )

        return saved_review
