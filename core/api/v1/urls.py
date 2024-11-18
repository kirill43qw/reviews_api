from ninja import Router

from core.api.v1.categories.handlers import router as category_router
from core.api.v1.customers.handlers import router as customer_router
from core.api.v1.genres.handlers import router as genre_router
from core.api.v1.titles.handlers import router as title_router
from core.api.v1.reviews.handlers import router as review_router
from core.api.v1.comments.handlers import router as comment_router
from core.api.v1.users.handlers import router as user_router

router = Router(tags=["v1"])

title_router.add_router("", review_router)
title_router.add_router("", comment_router)

router.add_router("", customer_router)
router.add_router("categories/", category_router)
router.add_router("genres/", genre_router)
router.add_router("titles/", title_router)
router.add_router("users/", user_router)
