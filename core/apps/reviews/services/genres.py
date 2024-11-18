from abc import ABC, abstractmethod
from typing import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.apps.reviews.entities import GenreEntity
from core.apps.reviews.exceptions.genre import GenreNotFound
from core.apps.reviews.filters.genres import GenreFilters
from core.apps.reviews.models.genres import Genre as GenreDTO


class BaseGenreService(ABC):
    @abstractmethod
    def get_genre_list(
        self, filters: GenreFilters, pagination: PaginationIn
    ) -> Iterable[GenreEntity]: ...

    @abstractmethod
    def get_genre_count(self, filters: GenreFilters) -> int: ...

    @abstractmethod
    def save_genre(self, genre_data: GenreEntity) -> GenreEntity: ...

    @abstractmethod
    def delete_genre(self, genre_id: int) -> GenreEntity: ...


class ORMGenreService(BaseGenreService):
    def _build_genre_query(self, filters: GenreFilters) -> Q:
        query = Q()
        if filters.search is not None:
            query = Q(title__icontains=filters.search)
        return query

    def get_genre_list(
        self, filters: GenreFilters, pagination: PaginationIn
    ) -> Iterable[GenreEntity]:
        query = self._build_genre_query(filters)
        qs = GenreDTO.objects.filter(query)[
            pagination.offset : pagination.offset + pagination.limit
        ]
        return [genre.to_entity() for genre in qs]

    def get_genre_count(self, filters: GenreFilters) -> int:
        query = self._build_genre_query(filters)
        return GenreDTO.objects.filter(query).count()

    def save_genre(self, genre_data: GenreEntity) -> GenreEntity:
        genre_dto = GenreDTO.from_entity(genre=genre_data)
        genre_dto.save()
        return genre_dto.to_entity()

    def delete_genre(self, genre_id: int) -> GenreEntity:
        try:
            genre_dto = GenreDTO.objects.get(id=genre_id)
            genre_dto.delete()
        except GenreDTO.DoesNotExist:
            raise GenreNotFound(genre_id=genre_id)
        return genre_dto.to_entity()
