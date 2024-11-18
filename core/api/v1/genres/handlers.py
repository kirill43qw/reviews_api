from django.http import HttpRequest
from ninja import Router, Query
from ninja.errors import HttpError

from core.api.filters import PaginationIn, PaginationOut
from core.api.schemas import ApiResponse, ListPaginatedResponse
from core.api.v1.genres.filters import GenreFilters
from core.api.v1.genres.schemas import (
    GenreDeleteSchema,
    GenreInSchema,
    GenreOutSchema,
    GenreSchema,
)
from core.apps.common.containers import get_container
from core.apps.common.exceptions import ServiceException
from core.apps.reviews.services.genres import BaseGenreService

from core.apps.reviews.filters.genres import (
    GenreFilters as GenreFiltersEntity,
)
from core.apps.reviews.use_cases.genre_create import CreateGenreUseCase


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


@router.post("", response=ApiResponse[GenreOutSchema], operation_id="createGenre")
def create_genre(request: HttpRequest, schema: GenreInSchema):
    container = get_container()
    use_case: CreateGenreUseCase = container.resolve(CreateGenreUseCase)
    try:
        result = use_case.execute(genre=schema.to_entity())
    except ServiceException as error:
        raise HttpError(status_code=400, message=error.message)
    return ApiResponse(data=GenreOutSchema.from_entity(result))


@router.delete(
    "{genre_id}/", response=ApiResponse[GenreDeleteSchema], operation_id="deleteGenre"
)
def delete_genre(request: HttpRequest, genre_id: int):
    container = get_container()
    service: BaseGenreService = container.resolve(BaseGenreService)
    try:
        del_genre = service.delete_genre(genre_id=genre_id)
    except ServiceException as error:
        raise HttpError(status_code=400, message=error.message)
    return ApiResponse(data=GenreDeleteSchema(id=genre_id, title=del_genre.title))
