from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from core.apps.common.models import TimedBaseModel
from core.apps.customers.models import Customer
from core.apps.reviews.models import Title
from core.apps.reviews.entities import ReviewEntity, TitleEntity
from core.apps.customers.entities import CustomerEntity


class Review(TimedBaseModel):
    author = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="оценка не может быть ниже 1"),
            MaxValueValidator(10, message="оценка не может быть выше 10"),
        ],
        verbose_name="оценка",
    )
    text = models.TextField()

    @classmethod
    def from_entity(
        cls,
        review: ReviewEntity,
        title: TitleEntity,
        customer: CustomerEntity,
    ) -> "Review":
        return cls(
            id=review.id,
            title_id=title.id,
            author_id=customer.id,
            rating=review.rating,
            text=review.text,
        )

    def to_entity(self) -> ReviewEntity:
        return ReviewEntity(
            id=self.id,
            text=self.text,
            rating=self.rating,
            created_at=self.created_at,
            updated_at=self.updated_at,
            title=self.title,
            author=self.author,
        )

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        # ordering = ("-created_at ",)
        constraints = [
            models.UniqueConstraint(fields=["author", "title"], name="unique_review")
        ]
