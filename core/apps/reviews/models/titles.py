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

    def to_entity(self) -> TitleEntity:
        return TitleEntity(
            id=self.id,
            title=self.title,
            rating=self.rating,
            year=self.year,
            description=self.description,
            category=self.category,
            genre=self.genre,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    class Meta:
        verbose_name = "Title"
        verbose_name_plural = "Titles"
        ordering = ("-year", "title")

        # unique_tigether = (('customer', 'title'))
        # один title на одного пользователя
