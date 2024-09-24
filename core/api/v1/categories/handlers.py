from django.http import HttpRequest
from ninja import Query, Router

from core.api.filters import PaginationIn
from core.api.schemas import ApiResponse, ListPaginatedResponse, PaginationOut
from core.api.v1.categories.schemas import CategorySchema
from core.api.v1.categories.filters import CategoryFilters
from core.apps.common.containers import get_container
from core.apps.reviews.filters.categories import (
    CategoryFilters as CategoryFiltersEntity,
)
from core.apps.reviews.services.categories import BaseCategoryService

router = Router(tags=["Categories"])


@router.get("", response=ApiResponse[ListPaginatedResponse[CategorySchema]])
def get_category_list_view(
    request: HttpRequest,
    filters: Query[CategoryFilters],
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[CategorySchema]]:
    container = get_container()
    service: BaseCategoryService = container.resolve(BaseCategoryService)
    # service: BaseCategoryService = ORMCategoryService()
    category_list = service.get_category_list(
        filters=CategoryFiltersEntity(search=filters.search),
        pagination=pagination_in,
    )
    category_count = service.get_category_count(filters=filters)
    items = [CategorySchema.from_entity(obj) for obj in category_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=category_count,
    )
    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out)
    )
