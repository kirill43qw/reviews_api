from django.http import HttpRequest
from ninja import Router, Query

from core.api.filters import PaginationIn
from core.api.schemas import ApiResponse, ListPaginatedResponse, PaginationOut
from core.api.v1.titles.filters import TitleFilters
from core.api.v1.titles.schemas import TitleSchema
from core.apps.common.containers import get_container
from core.apps.reviews.services.titles import BaseTitleService
from core.apps.reviews.filters.titles import TitleFilters as TitleFiltersEntity


router = Router(tags=["Titles"])


@router.get("", response=ApiResponse[ListPaginatedResponse[TitleSchema]])
def get_title_list(
    request: HttpRequest,
    filters: Query[TitleFilters],
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[TitleSchema]]:
    container = get_container()
    service: BaseTitleService = container.resolve(BaseTitleService)

    title_list = service.get_title_list(
        filters=TitleFiltersEntity(search=filters.search),
        pagination=pagination_in,
    )
    title_count = service.get_title_count(filters=filters)
    items = [TitleSchema.from_entity(obj) for obj in title_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=title_count,
    )
    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out)
    )
