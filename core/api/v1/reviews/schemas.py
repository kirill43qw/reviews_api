from datetime import datetime
from pydantic import BaseModel, field_validator

from core.apps.reviews.entities import ReviewEntity


class ReviewSchema(BaseModel):
    id: int
    text: str
    author: str
    rating: int
    updated_at: datetime

    @staticmethod
    def from_entity(entity: ReviewEntity) -> "ReviewSchema":
        return ReviewSchema(
            id=entity.id,
            text=entity.text,
            author=entity.author.username,
            rating=entity.rating,
            updated_at=entity.updated_at,
        )


class ReviewInSchema(BaseModel):
    text: str
    rating: int

    def to_entity(self):
        return ReviewEntity(text=self.text, rating=self.rating)


class ReviewUpdateSchema(BaseModel):
    text: str | None = None
    rating: int | None = None

    @field_validator("text", "rating")
    def replace_zero_with_none(cls, v):
        return v if v not in [0, "string"] else None

    def to_entity(self):
        return ReviewEntity(text=self.text, rating=self.rating)


class CreateReviewSchema(BaseModel):
    customer_token: int
    title_id: int
    review: ReviewInSchema


class ReviewOutSchema(ReviewInSchema):
    id: int
    author: str
    created_at: datetime
    updated_at: datetime | None = None

    @classmethod
    def from_entity(cls, review: ReviewEntity) -> "ReviewOutSchema":
        return cls(
            id=review.id,
            text=review.text,
            author=review.author.username,
            rating=review.rating,
            created_at=review.created_at,
            updated_at=review.updated_at,
        )
