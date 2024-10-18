from dataclasses import dataclass

from core.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class ReviewInvalidRating(ServiceException):
    rating: int

    @property
    def message(self):
        return "Rating is not valid. max 10, min 1"


@dataclass(eq=False)
class SingleReviewError(ServiceException):
    title_id: int
    author_id: int

    @property
    def message(self):
        return "User already posted a review on this title."
