from functools import lru_cache

from django.conf import settings
from httpx import Client
import punq

from core.apps.common.elasticsearch import ElasticClient
from core.apps.customers.services.auth import AuthService, BaseAuthService
from core.apps.customers.services.codes import BaseCodeService, DjangoCacheService
from core.apps.customers.services.customers import (
    BaseCustomersService,
    ORMCustomerService,
)
from core.apps.customers.services.sendors import (
    BaseSenderService,
    ComposeSenderService,
    PushSenderService,
    TelegramSenderService,
)
from core.apps.reviews.services.categories import (
    BaseCategoryService,
    ORMCategoryService,
)
from core.apps.reviews.services.genres import BaseGenreService, ORMGenreService
from core.apps.reviews.services.reviews import (
    BaseReviewService,
    BaseReviewValidatorService,
    ComposedReviewValidatorService,
    ORMReviewService,
    ReviewRatingValidatorService,
    SingleReviewValidatorService,
)
from core.apps.reviews.services.search import (
    BaseTitleSearchService,
    ElasticTitleSearchService,
)
from core.apps.reviews.services.titles import BaseTitleService, ORMTitleService
from core.apps.reviews.use_cases.review_create import CreateReviewUseCase
from core.apps.reviews.use_cases.upsert_search_data import UpsertSearchDataUseCase


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    def build_validators() -> BaseReviewValidatorService:
        return ComposedReviewValidatorService(
            validators=[
                container.resolve(SingleReviewValidatorService),
                container.resolve(ReviewRatingValidatorService),
            ]
        )

    def build_elastic_search_service() -> BaseTitleSearchService:
        return ElasticTitleSearchService(
            client=ElasticClient(http_client=Client(base_url=settings.ELASTIC_URL)),
            index_name=settings.ELASTIC_PRODUCT_INDEX,
        )

    # initialize services
    container.register(BaseCategoryService, ORMCategoryService)
    container.register(BaseGenreService, ORMGenreService)
    container.register(BaseReviewService, ORMReviewService)
    container.register(BaseTitleService, ORMTitleService)
    container.register(BaseTitleSearchService, factory=build_elastic_search_service)
    container.register(SingleReviewValidatorService)
    container.register(ReviewRatingValidatorService)
    container.register(BaseCustomersService, ORMCustomerService)
    container.register(BaseCodeService, DjangoCacheService)
    container.register(
        BaseSenderService,
        ComposeSenderService,
        sender_services=(
            PushSenderService(),
            TelegramSenderService(secret_key="check"),
        ),
    )
    container.register(BaseAuthService, AuthService)
    container.register(BaseReviewValidatorService, factory=build_validators)

    # init user cases
    container.register(UpsertSearchDataUseCase)
    container.register(CreateReviewUseCase)

    return container
