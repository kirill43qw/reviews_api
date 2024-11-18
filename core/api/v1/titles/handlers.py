from django.http import HttpRequest, HttpResponse
from ninja import Router, Query, Header
from ninja.errors import HttpError

from core.api.filters import PaginationIn
from core.api.schemas import ApiResponse, ListPaginatedResponse, PaginationOut
from core.api.v1.titles.filters import TitleFilters
from core.api.v1.titles.schemas import (
    TitleInSchema,
    TitleOutSchema,
    TitleSchema,
    TitleUpdateSchema,
)
from core.apps.common.containers import get_container
from core.apps.common.exceptions import ServiceException
from core.apps.reviews.services.titles import BaseTitleService
from core.apps.reviews.filters.titles import TitleFilters as TitleFiltersEntity
from core.apps.reviews.use_cases.title_dto import (
    UpdateTitleUseCase,
    CreateTitleUseCase,
    DeleteTitleUseCase,
)


router = Router(tags=["Titles"])
container = get_container()


@router.get("", response=ApiResponse[ListPaginatedResponse[TitleSchema]])
def get_title_list(
    request: HttpRequest,
    filters: Query[TitleFilters],
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[TitleSchema]]:
    service: BaseTitleService = container.resolve(BaseTitleService)

    title_list = service.get_title_list(
        filters=TitleFiltersEntity(search=filters.search),
        pagination=pagination_in,
    )
    items = [TitleSchema.from_entity(obj) for obj in title_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=len(items),
    )
    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out)
    )


@router.get("{title_id}/", response=ApiResponse[TitleSchema])
def get_title(request: HttpRequest, title_id: int):
    service: BaseTitleService = container.resolve(BaseTitleService)
    try:
        title = service.get_by_id(title_id=title_id)
    except ServiceException as error:
        raise HttpError(status_code=400, message=error.message)
    return ApiResponse(data=TitleSchema.from_entity(title))


@router.post("", response=ApiResponse[TitleOutSchema], operation_id="createTitle")
def create_title(
    request: HttpRequest, schema: TitleInSchema, token: str = Header(alias="Auth-Token")
):
    use_case: CreateTitleUseCase = container.resolve(CreateTitleUseCase)
    try:
        result = use_case.execute(token=token, title=schema.to_entity())
    except ServiceException as error:
        raise HttpError(status_code=400, message=error.message)
    return ApiResponse(
        data=TitleOutSchema.from_entity(result),
        meta={"message": "it's okay :)"},
    )


@router.patch(
    "{title_id}/", response=ApiResponse[TitleOutSchema], operation_id="updateTitle"
)
def update_title(
    request: HttpRequest,
    title_id: int,
    schema: TitleUpdateSchema,
    token: str = Header(alias="Auth-Token"),
):
    use_case: UpdateTitleUseCase = container.resolve(UpdateTitleUseCase)
    try:
        result = use_case.execute(
            token=token, title_id=title_id, title_data=schema.to_entity()
        )
    except ServiceException as error:
        raise HttpError(status_code=400, message=error.message)
    return ApiResponse(data=TitleOutSchema.from_entity(result))


@router.delete("{title_id}/", operation_id="deleteTitle")
def delete_title(
    request: HttpRequest, title_id: int, token: str = Header(alias="Auth-Token")
):
    use_case: DeleteTitleUseCase = container.resolve(DeleteTitleUseCase)
    try:
        use_case.execute(token=token, title_id=title_id)
    except ServiceException as error:
        raise HttpError(status_code=error.status_code, message=error.message)
    return HttpResponse(status=204)
