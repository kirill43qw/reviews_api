from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.customers.entities import CustomerEntity
from core.apps.customers.models import Customer
from core.apps.reviews.entities import CommentEntity
from core.apps.reviews.models import Review


class Comment(TimedBaseModel):
    review = models.ForeignKey(
        Review, verbose_name="Review", on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField(
        verbose_name="Comment",
    )
    author = models.ForeignKey(
        Customer,
        verbose_name="Author",
        on_delete=models.CASCADE,
        related_name="comments",
    )

    @classmethod
    def from_entity(
        cls, author: CustomerEntity, review_id: int, comment: CommentEntity
    ) -> "Comment":
        return cls(
            id=comment.id,
            text=comment.text,
            author_id=author.id,
            review_id=review_id,
        )

    def to_entity(self, review_id=None, author=None) -> CommentEntity:
        return CommentEntity(
            id=self.id,
            text=self.text,
            review=review_id or self.review,
            author=author or self.author,
        )

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["created_at"]
