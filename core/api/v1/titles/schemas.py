from pydantic import BaseModel, Field, field_validator
from datetime import datetime

from core.apps.reviews.entities import TitleEntity


class TitleInSchema(BaseModel):
    # прописать волидатоор на необязательные значения
    title: str
    description: str
    year: int
    category_id: int | None = Field(None, description="Category ID")
    genre_ids: list[int] = Field(default_factory=list, description="List Genre ID")

    def to_entity(self):
        return TitleEntity(
            title=self.title,
            description=self.description,
            year=self.year,
            category_id=self.category_id,
            genre_ids=self.genre_ids,
        )


class TitleUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    year: int | None = None
    category_id: int | None = Field(None, description="Category ID")
    genre_ids: list[int] | None = Field(None, description="List Genre IDs")

    @field_validator(
        "title", "description", "year", "category_id", "genre_ids", mode="before"
    )
    def replace_zero_with_none(cls, v):
        return v if v not in [0, "string"] and v != [0] else None

    def to_entity(self) -> TitleEntity:
        return TitleEntity(
            title=self.title,
            description=self.description,
            year=self.year,
            category_id=self.category_id,
            genre_ids=self.genre_ids,
        )


class TitleSchema(BaseModel):
    id: int
    title: str
    description: str
    rating: int | None
    year: int
    category_id: int | None
    genre_ids: list[int] = []

    @staticmethod
    def from_entity(entity: TitleEntity) -> "TitleSchema":
        return TitleSchema(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            rating=entity.rating,
            year=entity.year,
            category_id=entity.category_id,
            genre_ids=entity.genre_ids,
        )


class TitleOutSchema(TitleInSchema):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    @classmethod
    def from_entity(cls, title: TitleEntity) -> "TitleOutSchema":
        return cls(
            id=title.id,
            title=title.title,
            description=title.description,
            year=title.year,
            created_at=title.created_at,
            updated_at=title.updated_at,
            category_id=title.category_id,
            genre_ids=title.genre_ids,
        )
