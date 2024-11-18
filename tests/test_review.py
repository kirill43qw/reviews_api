import pytest

from core.apps.reviews.entities.reviews import ReviewEntity


@pytest.mark.django_db
def test_create_review_success(create_review_use_case, user, title):
    """Test successful creation of a review"""
    review_data = ReviewEntity(rating=8, text="Great title!")
    result = create_review_use_case.execute(
        customer_token=user.token,
        title_id=title.id,
        review=review_data,
    )

    assert result.rating == 8
    assert result.text == "Great title!"
    assert result.author.id == user.id
    assert result.title.id == title.id


# @pytest.mark.django_db
# def test_check_count_queries(
#     django_assert_num_queries, create_review_use_case, user, title
# ):
#     review_data = ReviewEntity(rating=8, text="Great title!")
#     with django_assert_num_queries(2):
#         create_review_use_case.execute(
#             customer_token=user.token,
#             title_id=title.id,
#             review=review_data,
#         )
