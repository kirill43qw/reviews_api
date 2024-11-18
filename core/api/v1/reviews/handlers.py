from django.http import HttpRequest, HttpResponse
from ninja import Header, Router, Query
from ninja.errors import HttpError

from core.api.filters import PaginationIn, PaginationOut
from core.api.schemas import ApiResponse, ListPaginatedResponse
from core.api.v1.reviews.schemas import (
    ReviewInSchema,
    ReviewOutSchema,
    ReviewSchema,
    ReviewUpdateSchema,
)
from core.apps.common.containers import get_container
from core.apps.common.exceptions import ServiceException
from core.apps.reviews.services.reviews import BaseReviewService
from core.apps.reviews.use_cases.review_dto import (
    CreateReviewUseCase,
    DeleteReviewUseCase,
    UpdateReviewUseCase,
)


router = Router(tags=["Review"])
container = get_container()


@router.get(
    "{title_id}/reviews/",
    response=ApiResponse[ListPaginatedResponse[ReviewSchema]],
)
def get_list_review(
    request: HttpRequest, title_id: int, pagination_in: Query[PaginationIn]
) -> ApiResponse[ListPaginatedResponse[ReviewSchema]]:
    service: BaseReviewService = container.resolve(BaseReviewService)
    review_list = service.get_review_list(title_id=title_id, pagination=pagination_in)
    items = [ReviewSchema.from_entity(obj) for obj in review_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=len(items),
    )
    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out)
    )


@router.get("{title_id}/reviews/{review_id}/", response=ApiResponse[ReviewSchema])
def get_review(request: HttpRequest, title_id: int, review_id: int):
    service: BaseReviewService = container.resolve(BaseReviewService)
    try:
        review = service.get_by_id(review_id=review_id)
    except ServiceException as error:
        raise HttpError(status_code=404, message=error.message)
    return ApiResponse(data=ReviewSchema.from_entity(review))


@router.post(
    "{title_id}/reviews/",
    response=ApiResponse[ReviewOutSchema],
    operation_id="createReview",
)
def cteate_review(
    request: HttpRequest,
    title_id: int,
    schema: ReviewInSchema,
    token: str = Header(alias="Auth-Token"),
) -> ApiResponse[ReviewOutSchema]:
    use_case: CreateReviewUseCase = container.resolve(CreateReviewUseCase)
    try:
        result = use_case.execute(
            customer_token=token,
            title_id=title_id,
            review=schema.to_entity(),
        )
    except ServiceException as error:
        raise HttpError(status_code=400, message=error.message)
    return ApiResponse(data=ReviewOutSchema.from_entity(result))


@router.patch(
    "{title_id}/reviews/{review_id}/",
    response=ApiResponse[ReviewOutSchema],
    operation_id="updateReview",
)
def update_review(
    request: HttpRequest,
    title_id: int,
    review_id: int,
    schema: ReviewUpdateSchema,
    token: str = Header(alias="Auth-Token"),
):
    use_case: UpdateReviewUseCase = container.resolve(UpdateReviewUseCase)
    try:
        result = use_case.execute(
            customer_token=token, review_id=review_id, review_data=schema.to_entity()
        )
    except ServiceException as error:
        raise HttpError(status_code=404, message=error.message)
    return ApiResponse(data=ReviewOutSchema.from_entity(result))


@router.delete("{title_id}/reviews/{review_id}/", operation_id="deleteReview")
def delete_review(
    request: HttpRequest,
    title_id: int,
    review_id: int,
    token: str = Header(alias="Auth-Token"),
):
    use_case: DeleteReviewUseCase = container.resolve(DeleteReviewUseCase)
    try:
        use_case.execute(customer_token=token, review_id=review_id)
    except ServiceException as error:
        raise HttpError(status_code=403, message=error.message)
    return HttpResponse(status=204)
