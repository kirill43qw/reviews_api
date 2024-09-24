from abc import ABC, abstractmethod
from typing import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.apps.reviews.entities import GenreEntity
from core.apps.reviews.filters.genres import GenreFilters
from core.apps.reviews.models.genres import Genre as GenreDTO


class BaseGenreService(ABC):
    @abstractmethod
    def get_genre_list(
        self, filters: GenreFilters, pagination: PaginationIn
    ) -> Iterable[GenreEntity]: ...

    @abstractmethod
    def get_genre_count(self, filters: GenreFilters) -> int: ...


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
