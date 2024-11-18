from django.http import HttpRequest, HttpResponse
from ninja import Query, Router, Header
from ninja.errors import HttpError

from core.api.filters import PaginationIn
from core.api.schemas import ApiResponse, ListPaginatedResponse, PaginationOut
from core.api.v1.categories.schemas import (
    CategoryDeleteSchema,
    CategoryInSchema,
    CategoryOutSchema,
    CategorySchema,
)
from core.api.v1.categories.filters import CategoryFilters
from core.apps.common.containers import get_container
from core.apps.common.exceptions import ServiceException
from core.apps.reviews.filters.categories import (
    CategoryFilters as CategoryFiltersEntity,
)
from core.apps.reviews.services.categories import BaseCategoryService
from core.apps.reviews.use_cases.category_crud import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
)

container = get_container()
router = Router(tags=["Categories"])


@router.get("", response=ApiResponse[ListPaginatedResponse[CategorySchema]])
def get_category_list_view(
    request: HttpRequest,
    filters: Query[CategoryFilters],
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[CategorySchema]]:
    service: BaseCategoryService = container.resolve(BaseCategoryService)
    category_list = service.get_category_list(
        filters=CategoryFiltersEntity(search=filters.search),
        pagination=pagination_in,
    )
    items = [CategorySchema.from_entity(obj) for obj in category_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=len(items),
    )
    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out)
    )


@router.post("", response=ApiResponse[CategoryOutSchema], operation_id="createCategory")
def create_category(
    request: HttpRequest,
    schema: CategoryInSchema,
    token: str = Header(alias="Auth-Token"),
):
    use_case: CreateCategoryUseCase = container.resolve(CreateCategoryUseCase)
    try:
        result = use_case.execute(token=token, category=schema.to_entity())
    except ServiceException as error:
        raise HttpError(status_code=error.status_code, message=error.message)
    return ApiResponse(data=CategoryOutSchema.from_entity(result))


@router.delete(
    "{category_id}/",
    response=ApiResponse[CategoryDeleteSchema],
    operation_id="deleteCategory",
)
def delete_category(
    request: HttpRequest, category_id: int, token: str = Header(alias="Auth-Token")
):
    use_case: DeleteCategoryUseCase = container.resolve(DeleteCategoryUseCase)
    try:
        use_case.execute(token=token, category_id=category_id)
    except ServiceException as error:
        raise HttpError(status_code=error.status_code, message=error.message)
    return HttpResponse(status=204)
