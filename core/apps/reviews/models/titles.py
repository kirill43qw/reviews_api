from datetime import datetime
from django.db import models
from core.apps.common.models import TimedBaseModel
from django.core.validators import MinValueValidator, MaxValueValidator

from core.apps.reviews.models import Category, Genre
from core.apps.reviews.entities import TitleEntity


class Title(TimedBaseModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="titles",
        verbose_name="Категория",
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        verbose_name="Жанр",
    )
    title = models.CharField(max_length=50)
    rating = models.IntegerField(null=True, default=None)
    year = models.IntegerField(
        validators=[
            MinValueValidator(
                1300, message="Настолько старые произведения не сохранились"
            ),
            MaxValueValidator(
                int(datetime.now().year), message="Год не может быть больше текущего"
            ),
        ]
    )
    description = models.TextField(verbose_name="Описание", null=True, blank=True)

    def __str__(self):
        return self.title

    @classmethod
    def from_entity(cls, title: TitleEntity) -> "Title":
        instance = cls(
            id=title.id,
            title=title.title,
            rating=title.rating,
            year=title.year,
            description=title.description,
            category_id=title.category_id,
            created_at=title.created_at,
            updated_at=title.updated_at,
        )
        instance.save()
        instance.genre.set(title.genre_ids)
        return instance

    def to_entity(self) -> TitleEntity:
        category_id = self.category.id if self.category else None
        genre_ids = list(self.genre.values_list("id", flat=True))

        return TitleEntity(
            id=self.id,
            title=self.title,
            rating=self.rating,
            year=self.year,
            description=self.description,
            category_id=category_id,
            genre_ids=genre_ids,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    class Meta:
        verbose_name = "Title"
        verbose_name_plural = "Titles"
        ordering = ("-year", "title")

        # unique_tigether = (('customer', 'title'))
        # один title на одного пользователя
