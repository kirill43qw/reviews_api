from dataclasses import dataclass

from core.apps.common.exceptions import ServiceException


@dataclass
class NoEmptyComment(ServiceException):

    @property
    def message(self):
        return "comment cannot be empty"


@dataclass
class NoCommentsFound(ServiceException):
    review_id: int

    @property
    def message(self):
        return "No comments found for this review"


@dataclass
class CommentNotFound(ServiceException):
    comment_id: int

    @property
    def message(self):
        return "Comment not found!"
