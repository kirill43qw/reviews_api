from django.http import HttpRequest
from ninja import Header, Router, Query
from ninja.errors import HttpError

from core.api.filters import PaginationIn, PaginationOut
from core.api.schemas import ApiResponse, ListPaginatedResponse
from core.api.v1.users.filter import UserFilter
from core.api.v1.users.schemas import UserSchema
from core.apps.common.containers import get_container
from core.apps.customers.services.customers import BaseCustomersService
from core.apps.customers.filters import UserFilters as UserFiltersEntity


router = Router(tags=["Users"])
container = get_container()


@router.get("", response=ApiResponse[ListPaginatedResponse[UserSchema]])
def get_list_user(
    request: HttpRequest,
    filters: Query[UserFilter],
    pagination_in: Query[PaginationIn],
    token: str = Header(alias="Auth-Token"),
):
    service: BaseCustomersService = container.resolve(BaseCustomersService)
    users_list = service.get_all_users(
        filters=UserFiltersEntity(search=filters.search), pagination=pagination_in
    )
    items = [UserSchema.from_entity(obj) for obj in users_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset, limit=pagination_in.limit, total=len(items)
    )
    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out)
    )
