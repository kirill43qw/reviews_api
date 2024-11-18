from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterator

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
    ) -> list[TitleEntity]: ...

    @abstractmethod
    def get_by_id(self, title_id: int) -> TitleDTO: ...

    @abstractmethod
    def get_all_title(self) -> Iterator[TitleEntity]: ...

    @abstractmethod
    def create_title(self, title_data: TitleEntity) -> TitleEntity: ...

    @abstractmethod
    def update_title(
        self, title_dto: TitleDTO, title_data: TitleEntity
    ) -> TitleEntity: ...

    @abstractmethod
    def delete_title(self, title_dto: TitleDTO) -> None: ...


class ORMTitleService(BaseTitleService):
    def _build_title_query(self, filters: TitleFilters) -> Q:
        query = Q()

        if filters.search is not None:
            ids = search_with_elastic(filters.search)
            query = Q(id__in=ids)

        return query

    def get_title_list(
        self, filters: TitleFilters, pagination: PaginationIn
    ) -> list[TitleEntity]:
        query = self._build_title_query(filters)
        qs = TitleDTO.objects.filter(query)[
            pagination.offset : pagination.offset + pagination.limit
        ]
        return [title.to_entity() for title in qs]

    def get_by_id(self, title_id: int) -> TitleDTO:
        try:
            return TitleDTO.objects.get(id=title_id)
        except TitleDTO.DoesNotExist:
            raise TitleNotFound(title_id=title_id)

    def get_all_title(self) -> Iterator[TitleEntity]:
        query = self._build_title_query(TitleFilters())
        queryset = TitleDTO.objects.filter(query)

        for title in queryset:
            yield title.to_entity()

    def create_title(self, title_data: TitleEntity) -> TitleEntity:
        title_dto = TitleDTO.from_entity(title=title_data)
        title_dto.save()
        return title_dto.to_entity()

    def update_title(self, title_dto: TitleDTO, title_data: TitleEntity) -> TitleEntity:
        fields_to_update = {
            "title": title_data.title,
            "description": title_data.description,
            "year": title_data.year,
            "category_id": title_data.category_id,
        }

        for field, value in fields_to_update.items():
            if value is not None:
                setattr(title_dto, field, value)

        if title_data.genre_ids is not None:
            title_dto.genre.set(title_data.genre_ids)

        title_dto.updated_at = datetime.now()
        title_dto.save()

        return title_dto.to_entity()

    def delete_title(self, title_dto: TitleDTO) -> None:
        title_dto.delete()
