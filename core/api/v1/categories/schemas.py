from datetime import datetime

from slugify import slugify
from pydantic import BaseModel

from core.apps.reviews.entities import CategoryEntity


class CategoryInSchema(BaseModel):
    title: str

    def generate_slug(self):
        return slugify(self.title, max_length=20)

    def to_entity(self):
        slug = self.generate_slug()
        return CategoryEntity(title=self.title, slug=slug)


class CategorySchema(BaseModel):
    id: int
    title: str
    slug: str
    updated_at: datetime | None = None

    @staticmethod
    def from_entity(entity: CategoryEntity) -> "CategorySchema":
        return CategorySchema(
            id=entity.id,
            title=entity.title,
            slug=entity.slug,
            updated_at=entity.updated_at,
        )


class CategoryOutSchema(CategoryInSchema):
    slug: str
    created_at: datetime
    updated_at: datetime | None = None

    @classmethod
    def from_entity(cls, category: CategoryEntity) -> "CategoryOutSchema":
        return cls(
            title=category.title,
            slug=category.slug,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )


class CategoryDeleteSchema(BaseModel):
    id: int
    title: str
