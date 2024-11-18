from dataclasses import dataclass

from core.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class GenreNotFound(ServiceException):
    genre_id: int

    @property
    def message(self):
        return "Genre not found &&"
