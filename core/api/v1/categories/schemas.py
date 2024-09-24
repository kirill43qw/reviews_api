from datetime import datetime

from pydantic import BaseModel

from core.apps.reviews.entities import CategoryEntity


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
