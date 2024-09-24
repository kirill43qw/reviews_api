from django.http import HttpRequest
from ninja import Header, Router
from ninja.errors import HttpError

from core.api.schemas import ApiResponse
from core.api.v1.reviews.schemas import ReviewInSchema, ReviewOutSchema
from core.apps.common.containers import get_container
from core.apps.common.exceptions import ServiceException
from core.apps.reviews.use_cases.review_create import CreateReviewUseCase


router = Router(tags=["Review"])


@router.post(
    "{title_id}/reviews",
    response=ApiResponse[ReviewOutSchema],
    operation_id="createReview",
)
def cteate_review(
    request: HttpRequest,
    title_id: int,
    schema: ReviewInSchema,
    token: str = Header(alias="Auth-Token"),
) -> ApiResponse[ReviewOutSchema]:
    container = get_container()
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
