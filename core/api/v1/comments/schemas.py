from datetime import datetime

from pydantic import BaseModel, field_validator

from core.apps.reviews.entities.comments import CommentEntity


class CommentSchema(BaseModel):
    id: int
    text: str
    author: str
    updated_at: datetime | None = None

    @staticmethod
    def from_entity(entity: CommentEntity) -> "CommentSchema":
        return CommentSchema(
            id=entity.id,
            text=entity.text,
            author=entity.author.username,
            updated_at=entity.updated_at or entity.created_at,
        )


class CommentInSchema(BaseModel):
    text: str

    @field_validator("text")
    def text_cannot_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Comment text cannot be empty")
        return value

    def to_entity(self):
        return CommentEntity(text=self.text)


class CommentOutSchema(BaseModel):
    id: int
    text: str
    author: str
    created_at: datetime

    @classmethod
    def from_entity(cls, comment: CommentEntity) -> "CommentOutSchema":
        return cls(
            id=comment.id,
            text=comment.text,
            author=comment.author.username,
            created_at=comment.created_at,
        )
