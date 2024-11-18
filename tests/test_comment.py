import pytest
from core.apps.customers.exceptions.customers import CustomerTokenInvalid
from core.apps.reviews.exceptions.comment import CommentNotFound
from tests.factories.comment import CommentModelFactory


@pytest.mark.django_db
def test_create_comment_queries(
    django_assert_num_queries, create_comment_use_case, user, review, comment_data
):
    """Test that updating a comment only triggers the expected number of queries"""
    with django_assert_num_queries(2):
        create_comment_use_case.execute(
            customer_token=user.token,
            review_id=review.id,
            comment_data=comment_data,
        )


@pytest.mark.django_db
def test_create_comment(create_comment_use_case, user, review, comment_data):
    """Test for creating a comment"""
    result = create_comment_use_case.execute(
        customer_token=user.token, review_id=review.id, comment_data=comment_data
    )

    assert result.text == "check_comment"
    assert result.author.id == user.id


@pytest.mark.django_db
def test_create_noauthorize_user(create_comment_use_case, comment_data, review):
    """test for creating a comment by a non-existent user"""
    with pytest.raises(CustomerTokenInvalid):
        create_comment_use_case.execute(
            customer_token="lafda239fjlbawk",
            review_id=review.id,
            comment_data=comment_data,
        )


@pytest.mark.django_db
def test_update_comment_author_comment(
    update_comment_use_case, user, comment, comment_data
):
    """Test to check if a comment has been updated, the author is the owner of the comment"""
    result = update_comment_use_case.execute(
        customer_token=user.token,
        comment_id=comment.id,
        comment_data=comment_data,
    )

    assert result.text == comment_data.text
    assert result.author.id == user.id


@pytest.mark.django_db
def test_update_comment_queries(
    django_assert_num_queries, update_comment_use_case, user, comment, comment_data
):
    """Test that updating a comment only triggers the expected number of queries"""
    with django_assert_num_queries(3):
        update_comment_use_case.execute(
            customer_token=user.token,
            comment_id=comment.id,
            comment_data=comment_data,
        )


@pytest.mark.django_db
def test_update_comment_administrator(
    update_comment_use_case, user, admin, comment, comment_data
):
    """Test for updating comment by administrator"""
    result = update_comment_use_case.execute(
        customer_token=admin.token,
        comment_id=comment.id,
        comment_data=comment_data,
    )

    assert result.text == comment_data.text
    assert result.author.id == user.id


@pytest.mark.django_db
def test_update_comment__moderaot(
    update_comment_use_case, user, moderator, comment, comment_data
):
    """Test for updating comment by moderator"""
    result = update_comment_use_case.execute(
        customer_token=moderator.token,
        comment_id=comment.id,
        comment_data=comment_data,
    )

    assert result.text == comment_data.text
    assert result.author.id == user.id


@pytest.mark.django_db
def test_update_comment_no_author(update_comment_use_case, user, comment_data):
    """Test to verify that a normal user cannot update their comment"""
    other_comment = CommentModelFactory()

    with pytest.raises(PermissionError):
        update_comment_use_case.execute(
            customer_token=user.token,
            comment_id=other_comment.id,
            comment_data=comment_data,
        )


@pytest.mark.django_db
def test_delete_comment_author_comment(
    delete_comment_use_case, comment_service, user, comment
):
    """Test to delete a comment, the user is the author of the comment"""
    delete_comment_use_case.execute(customer_token=user.token, comment_id=comment.id)

    with pytest.raises(CommentNotFound):
        comment_service.get_by_id(comment.id)


@pytest.mark.django_db
def test_delete_comment_unauthorized_user(delete_comment_use_case, user):
    """Test to delete a comment, the user is not the author of the comment"""
    other_comment = CommentModelFactory()

    with pytest.raises(PermissionError):
        delete_comment_use_case.execute(
            customer_token=user.token, comment_id=other_comment.id
        )


@pytest.mark.django_db
def test_delete_comment_adminisrator(
    delete_comment_use_case, comment_service, admin, comment
):
    """test of deleting a comment by an administrator"""
    delete_comment_use_case.execute(customer_token=admin.token, comment_id=comment.id)

    with pytest.raises(CommentNotFound):
        comment_service.get_by_id(comment.id)


@pytest.mark.django_db
def test_delete_comment_moderator(
    delete_comment_use_case, comment_service, moderator, comment
):
    """test of deleting a comment by an moderator"""
    delete_comment_use_case.execute(
        customer_token=moderator.token, comment_id=comment.id
    )

    with pytest.raises(CommentNotFound):
        comment_service.get_by_id(comment.id)


@pytest.mark.django_db
def test_delete_nonexistent_comment(delete_comment_use_case, user):
    """Test to remove non-existent comment"""
    with pytest.raises(CommentNotFound):
        delete_comment_use_case.execute(customer_token=user.token, comment_id=9999)


@pytest.mark.django_db
def test_delete_comment_queries(
    django_assert_num_queries, delete_comment_use_case, user, comment
):
    """Test that updating a comment only triggers the expected number of queries"""
    with django_assert_num_queries(3):
        delete_comment_use_case.execute(
            customer_token=user.token,
            comment_id=comment.id,
        )
