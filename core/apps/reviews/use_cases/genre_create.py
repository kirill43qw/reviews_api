from dataclasses import dataclass

from core.apps.reviews.entities.genres import GenreEntity
from core.apps.reviews.services.genres import BaseGenreService


@dataclass
class CreateGenreUseCase:
    genre_service: BaseGenreService

    def execute(self, genre: GenreEntity) -> GenreEntity:
        # validators
        save_genre = self.genre_service.save_genre(genre_data=genre)
        return save_genre
