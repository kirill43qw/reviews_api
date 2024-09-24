from functools import lru_cache

import punq

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
)
from core.apps.reviews.services.titles import BaseTitleService, ORMTitleService
from core.apps.reviews.use_cases.review_create import CreateReviewUseCase


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    # initialize category
    container.register(BaseCategoryService, ORMCategoryService)

    # initialize genre
    container.register(BaseGenreService, ORMGenreService)

    # initialize customers
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

    # initialize titles
    container.register(BaseTitleService, ORMTitleService)

    # initialize reviews
    container.register(BaseReviewService, ORMReviewService)
    container.register(
        BaseReviewValidatorService, ComposedReviewValidatorService, validators=[]
    )
    container.register(CreateReviewUseCase)

    return container
