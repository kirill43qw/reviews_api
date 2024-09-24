from dataclasses import dataclass

from core.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class TitleNotFound(ServiceException):
    title_id: int

    @property
    def message(self):
        return "Title not found"
