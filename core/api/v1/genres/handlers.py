from django.http import HttpRequest
from ninja import Router, Query

from core.api.filters import PaginationIn, PaginationOut
from core.api.schemas import ApiResponse, ListPaginatedResponse
from core.api.v1.genres.filters import GenreFilters
from core.api.v1.genres.schemas import GenreSchema
from core.apps.common.containers import get_container
from core.apps.reviews.services.genres import BaseGenreService

from core.apps.reviews.filters.genres import (
    GenreFilters as GenreFiltersEntity,
)


router = Router(tags=["Genres"])


@router.get("", response=ApiResponse[ListPaginatedResponse[GenreSchema]])
def get_genre_list_view(
    request: HttpRequest,
    filters: Query[GenreFilters],
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[GenreSchema]]:
    container = get_container()
    service: BaseGenreService = container.resolve(BaseGenreService)
    genre_list = service.get_genre_list(
        filters=GenreFiltersEntity(search=filters.search), pagination=pagination_in
    )
    genre_count = service.get_genre_count(filters=filters)
    items = [GenreSchema.from_entity(obj) for obj in genre_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset, limit=pagination_in.limit, total=genre_count
    )
    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out)
    )
