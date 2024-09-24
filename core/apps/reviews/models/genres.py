from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.reviews.entities import GenreEntity


class Genre(TimedBaseModel):
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30, unique=True)

    def to_entity(self) -> GenreEntity:
        return GenreEntity(
            id=self.id,
            title=self.title,
            slug=self.slug,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        ordering = ("title",)
