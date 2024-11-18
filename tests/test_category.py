import pytest

from core.api.filters import PaginationIn
from core.api.v1.filters import CategoryFilters
from core.apps.reviews.services.categories import BaseCategoryService
from tests.factories.category import CategoryModelFactory


@pytest.mark.django_db
def test_get_category_count_zero(category_service: BaseCategoryService):
    category_count = category_service.get_category_count(CategoryFilters())
    assert category_count == 0, f"{category_count=}"


@pytest.mark.django_db
def test_get_category_count_exists(category_service: BaseCategoryService):
    expected_count = 5
    CategoryModelFactory.create_batch(size=expected_count)
    category_count = category_service.get_category_count(CategoryFilters())
    assert category_count == expected_count, f"{category_count=}"


@pytest.mark.django_db
def test_get_all_categories(category_service: BaseCategoryService):
    expected_count = 5
    categories = CategoryModelFactory.create_batch(size=expected_count)
    categories_titles = {category.title for category in categories}

    fetched_categories = category_service.get_category_list(
        CategoryFilters(), PaginationIn()
    )
    fetched_titles = {category.title for category in fetched_categories}

    assert len(fetched_titles) == expected_count, f"{fetched_categories=}"
    assert categories_titles == fetched_titles, f"{categories_titles=}"
