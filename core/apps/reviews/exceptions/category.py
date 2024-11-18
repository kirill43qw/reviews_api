from dataclasses import dataclass

from core.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class CategoryNotFound(ServiceException):
    category_id: int

    @property
    def message(self):
        return "Category not found :("
