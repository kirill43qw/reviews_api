from abc import ABC, abstractmethod
from typing import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.apps.reviews.entities.categories import CategoryEntity
from core.apps.reviews.filters.categories import CategoryFilters
from core.apps.reviews.models.categories import Category as CategoryDTO


class BaseCategoryService(ABC):
    @abstractmethod
    def get_category_list(
        self, filters: CategoryFilters, pagination: PaginationIn
    ) -> Iterable[CategoryEntity]: ...

    @abstractmethod
    def get_category_count(self, filters: CategoryFilters) -> int: ...


class ORMCategoryService(BaseCategoryService):
    def _build_category_query(self, filters: CategoryFilters) -> Q:
        query = Q()
        if filters.search is not None:
            query = Q(title__icontains=filters.search)
        return query

    def get_category_list(
        self, filters: CategoryFilters, pagination: PaginationIn
    ) -> Iterable[CategoryEntity]:
        query = self._build_category_query(filters)
        qs = CategoryDTO.objects.filter(query)[
            pagination.offset : pagination.offset + pagination.limit
        ]
        return [category.to_entity() for category in qs]

    def get_category_count(self, filters: CategoryFilters) -> int:
        query = self._build_category_query(filters)
        return CategoryDTO.objects.filter(query).count()
