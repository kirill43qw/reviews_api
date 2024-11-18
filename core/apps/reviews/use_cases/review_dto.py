from dataclasses import dataclass

from core.apps.common.permission_service import PermissionService
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


@dataclass
class UpdateReviewUseCase:
    customer_service: BaseCustomersService
    review_service: BaseReviewService
    permission_service: PermissionService

    def execute(
        self, customer_token: str, review_id: int, review_data: ReviewEntity
    ) -> ReviewEntity:
        author = self.customer_service.get_by_token(token=customer_token)
        review = self.review_service.get_by_id(review_id=review_id)
        self.permission_service.permission_authorobj_admin_moderator(
            author=author, obj=review
        )
        updated_review = self.review_service.update_review(
            review=review, review_data=review_data
        )
        return updated_review


@dataclass
class DeleteReviewUseCase:
    customer_service: BaseCustomersService
    review_service: BaseReviewService
    permission_service: PermissionService

    def execute(self, customer_token: str, review_id: int):
        author = self.customer_service.get_by_token(token=customer_token)
        review = self.review_service.get_by_id(review_id=review_id)
        self.permission_service.permission_authorobj_admin_moderator(
            author=author, obj=review
        )
        self.review_service.delete_review(review=review)
