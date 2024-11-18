from abc import ABC, abstractmethod
from datetime import datetime

from core.api.filters import PaginationIn
from core.apps.customers.entities import CustomerEntity
from core.apps.reviews.entities.comments import CommentEntity
from core.apps.reviews.exceptions.comment import CommentNotFound, NoCommentsFound
from core.apps.reviews.models import Comment as CommentDTO


class BaseCommentService(ABC):
    @abstractmethod
    def get_comment_list(
        self, review_id: int, pagination: PaginationIn
    ) -> list[CommentEntity]: ...

    @abstractmethod
    def get_by_id(self, comment_id: int) -> CommentDTO: ...

    @abstractmethod
    def create_comment(
        self, author: CustomerEntity, review_id: int, comment_data: CommentEntity
    ) -> CommentEntity: ...

    @abstractmethod
    def update_comment(
        self, comment: CommentDTO, comment_data: CommentEntity
    ) -> CommentEntity: ...

    @abstractmethod
    def delete_comment(self, comment: CommentDTO) -> None: ...


class ORMCommentService(BaseCommentService):
    def get_comment_list(
        self, review_id: int, pagination: PaginationIn
    ) -> list[CommentEntity]:
        query = CommentDTO.objects.filter(review_id=review_id)[
            pagination.offset : pagination.offset + pagination.limit
        ]
        if not query.exists():
            raise NoCommentsFound(review_id=review_id)
        return [comment.to_entity() for comment in query]

    def get_by_id(self, comment_id: int) -> CommentDTO:
        try:
            return CommentDTO.objects.select_related("author", "review").get(
                id=comment_id
            )
        except CommentDTO.DoesNotExist:
            raise CommentNotFound(comment_id=comment_id)

    def create_comment(
        self, author: CustomerEntity, review_id: int, comment_data: CommentEntity
    ) -> CommentEntity:
        comment_dto = CommentDTO.from_entity(
            author=author, review_id=review_id, comment=comment_data
        )
        comment_dto.save()

        return comment_dto.to_entity(review_id=review_id, author=author)

    def update_comment(
        self, comment: CommentDTO, comment_data: CommentEntity
    ) -> CommentEntity:
        fields_to_update = {"text": comment_data.text}
        for field, value in fields_to_update.items():
            if value is not None:
                setattr(comment, field, value)
        comment.updated_at = datetime.now()
        comment.save()
        return comment.to_entity()

    def delete_comment(self, comment: CommentDTO) -> None:
        comment.delete()
