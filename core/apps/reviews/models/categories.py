from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.reviews.entities import CategoryEntity


class Category(TimedBaseModel):
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30, unique=True)

    def to_entity(self) -> CategoryEntity:
        return CategoryEntity(
            id=self.id,
            title=self.title,
            slug=self.slug,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_entity(cls, category: CategoryEntity) -> "Category":
        return cls(
            id=category.id,
            title=category.title,
            slug=category.slug,
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ("title",)
