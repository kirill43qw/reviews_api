import pytest

from core.api.filters import PaginationIn
from core.apps.reviews.exceptions.title import TitleNotFound
from core.apps.reviews.filters.titles import TitleFilters
from core.apps.reviews.services.titles import BaseTitleService
from tests.factories import TitleModelFactory, GenreModelFactory, CategoryModelFactory


@pytest.mark.django_db
def test_get_titles_count_zero(title_service: BaseTitleService):
    """title count zero with no title in database"""
    title_count = title_service.get_title_count(TitleFilters())
    assert title_count == 0, f"{title_count=}"


@pytest.mark.django_db
def test_get_titles_count_exist(title_service: BaseTitleService):
    """title count with existing titles in the database"""
    expected_count = 5
    TitleModelFactory.create_batch(size=expected_count)
    titles_count = title_service.get_title_count(TitleFilters())
    assert titles_count == expected_count, f"{titles_count=}"


@pytest.mark.django_db
def test_get_titles_all(title_service: BaseTitleService):
    """retrieving all titles from the database"""
    expected_count = 5
    titles = TitleModelFactory.create_batch(size=expected_count)
    titles_names = {title.title for title in titles}

    fetched_titles = title_service.get_title_list(TitleFilters(), PaginationIn())
    fetched_names = {title.title for title in fetched_titles}

    assert len(fetched_names) == expected_count, f"{fetched_names=}"
    assert titles_names == fetched_names, f"{titles_names=}"


@pytest.mark.django_db
def test_create_title(title_service: BaseTitleService):
    """creating title"""
    category = CategoryModelFactory()
    genres = GenreModelFactory.create_batch(size=2)
    title_instance = TitleModelFactory.create(category=category, genre=genres)
    title_data = title_instance.to_entity()

    created_title = title_service.create_title(title_data)
    print(created_title)

    assert created_title.title == title_data.title
    assert created_title.category_id == category.id
    assert set(created_title.genre_ids) == {genre.id for genre in genres}


@pytest.mark.django_db
def test_update_title(title_service: BaseTitleService):
    """updating title"""
    title = TitleModelFactory()
    new_title_name = "Updated Title"
    updated_data = title.to_entity()
    updated_data.title = new_title_name

    updated_title = title_service.update_title(title.id, updated_data)

    assert updated_title.title == new_title_name, f"{updated_title.title=}"
    assert updated_title.id == title.id


@pytest.mark.django_db
def test_delete_title(title_service: BaseTitleService):
    """Test remove title"""
    title = TitleModelFactory()
    title_service.delete_title(title_id=title.id)

    with pytest.raises(TitleNotFound):
        title_service.get_by_id(title_id=title.id)


@pytest.mark.django_db
def test_get_titles_with_pagination(title_service: BaseTitleService):
    """Test pagination"""
    TitleModelFactory.create_batch(size=10)

    pagination = PaginationIn(offset=0, limit=5)
    first_page_titles = title_service.get_title_list(TitleFilters(), pagination)
    assert len(first_page_titles) == 5

    pagination = PaginationIn(offset=5, limit=5)
    second_page_titles = title_service.get_title_list(TitleFilters(), pagination)
    assert len(second_page_titles) == 5

    first_titles_set = {title.id for title in first_page_titles}
    second_titles_set = {title.id for title in second_page_titles}
    assert first_titles_set.isdisjoint(second_titles_set)


@pytest.mark.django_db
def test_delete_nonexistent_title(title_service: BaseTitleService):
    """Checking the removal of a destructive object"""
    non_existent_id = 9999

    with pytest.raises(TitleNotFound):
        title_service.delete_title(title_id=non_existent_id)


@pytest.mark.django_db
def test_update_title_partial_fields(title_service: BaseTitleService):
    """Checking if only changed fields are updated"""
    title = TitleModelFactory()
    original_category_id = title.category.id if title.category else None

    updated_data = title.to_entity()
    updated_data.title = "Partially Updated Title"
    updated_data.category_id = original_category_id
    updated_data.description = None

    updated_title = title_service.update_title(title.id, updated_data)

    assert updated_title.title == "Partially Updated Title"
    assert updated_title.description == title.description
    assert updated_title.updated_at != title.updated_at
    assert updated_title.category_id == original_category_id
