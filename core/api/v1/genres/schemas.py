from datetime import datetime

from slugify import slugify
from pydantic import BaseModel

from core.apps.reviews.entities import GenreEntity


class GenreInSchema(BaseModel):
    title: str

    def generate_slug(self):
        return slugify(self.title, max_length=20)

    def to_entity(self):
        slug = self.generate_slug()
        return GenreEntity(title=self.title, slug=slug)


class GenreSchema(BaseModel):
    id: int
    title: str
    slug: str
    updated_at: datetime | None = None

    @staticmethod
    def from_entity(entity: GenreEntity) -> "GenreSchema":
        return GenreSchema(
            id=entity.id,
            title=entity.title,
            slug=entity.slug,
            updated_at=entity.updated_at,
        )


class GenreOutSchema(GenreInSchema):
    slug: str
    created_at: datetime
    updated_at: datetime | None = None

    @classmethod
    def from_entity(cls, genre: GenreEntity) -> "GenreOutSchema":
        return cls(
            title=genre.title,
            slug=genre.slug,
            created_at=genre.created_at,
            updated_at=genre.updated_at,
        )


class GenreDeleteSchema(BaseModel):
    id: int
    title: str
