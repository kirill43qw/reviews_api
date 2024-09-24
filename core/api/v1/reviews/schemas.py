from datetime import datetime
from pydantic import BaseModel

from core.apps.reviews.entities import ReviewEntity


class ReviewInSchema(BaseModel):
    text: str
    rating: int

    def to_entity(self):
        return ReviewEntity(text=self.text, rating=self.rating)


class CreateReviewSchema(BaseModel):
    customer_token: int
    title_id: int
    review: ReviewInSchema


class ReviewOutSchema(ReviewInSchema):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    @classmethod
    def from_entity(cls, review: ReviewEntity) -> "ReviewOutSchema":
        return cls(
            id=review.id,
            text=review.text,
            rating=review.rating,
            created_at=review.created_at,
            updated_at=review.updated_at,
        )
