from dataclasses import dataclass

from core.apps.common.permission_service import PermissionService
from core.apps.customers.services.customers import BaseCustomersService
from core.apps.reviews.entities.comments import CommentEntity
from core.apps.reviews.services.comments import BaseCommentService


@dataclass
class CreateCommentUseCase:
    customer_service: BaseCustomersService
    comment_service: BaseCommentService

    def execute(
        self,
        customer_token: str,
        review_id: int,
        comment_data: CommentEntity,
    ):
        author = self.customer_service.get_by_token(token=customer_token)
        saved_comment = self.comment_service.create_comment(
            author=author, review_id=review_id, comment_data=comment_data
        )
        return saved_comment


@dataclass
class UpdateCommentUseCase:
    customer_service: BaseCustomersService
    comment_service: BaseCommentService
    permission_service: PermissionService

    def execute(
        self, customer_token: str, comment_id: int, comment_data: CommentEntity
    ):
        author = self.customer_service.get_by_token(token=customer_token)
        comment = self.comment_service.get_by_id(comment_id=comment_id)

        self.permission_service.permission_authorobj_admin_moderator(
            author=author, obj=comment
        )

        updated_comment = self.comment_service.update_comment(
            comment=comment, comment_data=comment_data
        )
        return updated_comment


@dataclass
class DeleteCommentUseCase:
    customer_service: BaseCustomersService
    comment_service: BaseCommentService
    permission_service: PermissionService

    def execute(self, customer_token: str, comment_id: int):
        author = self.customer_service.get_by_token(token=customer_token)
        comment = self.comment_service.get_by_id(comment_id=comment_id)

        self.permission_service.permission_authorobj_admin_moderator(
            author=author, obj=comment
        )

        self.comment_service.delete_comment(comment=comment)
