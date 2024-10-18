from abc import ABC, abstractmethod
from typing import Iterable

import httpx
from django.db.models import Q

from core.api.filters import PaginationIn

from core.apps.common.elasticsearch import search_with_elastic
from core.apps.reviews.entities import TitleEntity
from core.apps.reviews.exceptions.title import TitleNotFound
from core.apps.reviews.filters.titles import TitleFilters
from core.apps.reviews.models import Title as TitleDTO


class BaseTitleService(ABC):
    @abstractmethod
    def get_title_list(
        self,
        filters: TitleFilters,
        pagination: PaginationIn,
    ) -> Iterable[TitleEntity]: ...

    @abstractmethod
    def get_title_count(self, filters: TitleFilters) -> int: ...

    @abstractmethod
    def get_by_id(self, title_id: int) -> int: ...

    @abstractmethod
    def get_all_title(self) -> Iterable[TitleEntity]: ...


class ORMTitleService(BaseTitleService):
    def _build_title_query(self, filters: TitleFilters) -> Q:
        query = Q()

        if filters.search is not None:
            ids = search_with_elastic(filters.search)
            query = Q(id__in=ids)

        return query

    def get_title_list(
        self, filters: TitleFilters, pagination: PaginationIn
    ) -> Iterable[TitleEntity]:
        query = self._build_title_query(filters)
        qs = TitleDTO.objects.filter(query)[
            pagination.offset : pagination.offset + pagination.limit
        ]
        return [title.to_entity() for title in qs]

    def get_title_count(self, filters: TitleFilters) -> int:
        query = self._build_title_query(filters)
        return TitleDTO.objects.filter(query).count()

    def get_by_id(self, title_id: int) -> int:
        try:
            title_dto = TitleDTO.objects.get(id=title_id)
        except TitleDTO.DoesNotExist:
            raise TitleNotFound(title_id=title_id)
        return title_dto.to_entity()

    def get_all_title(self) -> Iterable[TitleEntity]:
        query = self._build_title_query(TitleFilters())
        queryset = TitleDTO.objects.filter(query)

        for title in queryset:
            yield title.to_entity()
