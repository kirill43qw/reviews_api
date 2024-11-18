from django.http import HttpRequest, HttpResponse
from ninja import Router, Query, Header
from ninja.errors import HttpError

from core.api.filters import PaginationIn, PaginationOut
from core.api.schemas import ApiResponse, ListPaginatedResponse
from core.api.v1.comments.exceptions import handle_exceptions
from core.api.v1.comments.schemas import (
    CommentInSchema,
    CommentOutSchema,
    CommentSchema,
)
from core.apps.common.containers import get_container
from core.apps.common.exceptions import ServiceException
from core.apps.reviews.services.comments import BaseCommentService
from core.apps.reviews.use_cases.comment_crud import (
    CreateCommentUseCase,
    DeleteCommentUseCase,
    UpdateCommentUseCase,
)


router = Router(tags=["Comment"])
container = get_container()


@router.get(
    "{title_id}/reviews/{review_id}/comments/",
    response=ApiResponse[ListPaginatedResponse[CommentSchema]],
)
@handle_exceptions
def get_comments_list(
    request: HttpRequest,
    title_id: int,
    review_id: int,
    pagination_in: Query[PaginationIn],
):
    service: BaseCommentService = container.resolve(BaseCommentService)
    comment_list = service.get_comment_list(
        review_id=review_id, pagination=pagination_in
    )
    items = [CommentSchema.from_entity(obj) for obj in comment_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=len(items),
    )
    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out)
    )


@router.get(
    "{title_id}/reviews/{review_id}/comments/{comment_id}/",
    response=ApiResponse[CommentSchema],
)
@handle_exceptions
def get_comment(request: HttpRequest, title_id: int, review_id: int, comment_id: int):
    service: BaseCommentService = container.resolve(BaseCommentService)
    comment = service.get_by_id(comment_id=comment_id)
    return ApiResponse(data=CommentSchema.from_entity(comment))


@router.post(
    "{title_id}/reviews/{review_id}/comments/",
    response=ApiResponse[CommentOutSchema],
    operation_id="createComment",
)
@handle_exceptions
def create_comment(
    request: HttpRequest,
    title_id: int,
    review_id: int,
    schema: CommentInSchema,
    token: str = Header(alias="Auth-Token"),
):
    use_case: CreateCommentUseCase = container.resolve(CreateCommentUseCase)
    result = use_case.execute(
        customer_token=token, review_id=review_id, comment_data=schema.to_entity()
    )
    return ApiResponse(data=CommentOutSchema.from_entity(result))


@router.patch(
    "{title_id}/reviews/{review_id}/comments/{comment_id}/",
    response=ApiResponse[CommentOutSchema],
    operation_id="updateComment",
)
@handle_exceptions
def update_comment(
    request: HttpRequest,
    title_id: int,
    review_id: int,
    comment_id: int,
    schema: CommentInSchema,
    token: str = Header(alias="Auth-Token"),
):
    use_case: UpdateCommentUseCase = container.resolve(UpdateCommentUseCase)
    result = use_case.execute(
        customer_token=token, comment_id=comment_id, comment_data=schema.to_entity()
    )
    return ApiResponse(data=CommentOutSchema.from_entity(result))


@router.delete(
    "{title_id}/reviews/{review_id}/comments/{comment_id}/",
    operation_id="deleteComment",
)
# @handle_exceptions
def delete_comment(
    request: HttpRequest,
    title_id: int,
    review_id: int,
    comment_id: int,
    token: str = Header(alias="Auth-Token"),
):
    use_case: DeleteCommentUseCase = container.resolve(DeleteCommentUseCase)
    try:
        use_case.execute(customer_token=token, comment_id=comment_id)
    except ServiceException as error:
        raise HttpError(status_code=403, message=error.message)
    return HttpResponse(status=204)
