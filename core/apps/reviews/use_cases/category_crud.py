from dataclasses import dataclass

from core.apps.common.permission_service import PermissionService
from core.apps.customers.services.customers import BaseCustomersService
from core.apps.reviews.entities import CategoryEntity
from core.apps.reviews.services.categories import BaseCategoryService


@dataclass
class CreateCategoryUseCase:
    category_service: BaseCategoryService
    customer_service: BaseCustomersService
    permission_service: PermissionService

    def execute(self, token: str, category: CategoryEntity) -> CategoryEntity:
        author = self.customer_service.get_by_token(token=token)
        self.permission_service.permission_only_admin(author=author)
        # write validators
        saved_category = self.category_service.save_category(category_data=category)
        return saved_category


@dataclass
class DeleteCategoryUseCase:
    category_service: BaseCategoryService
    customer_service: BaseCustomersService
    permission_service: PermissionService

    def execute(self, token: str, category_id: int):
        author = self.customer_service.get_by_token(token=token)
        self.permission_service.permission_only_admin(author=author)
        category_dto = self.category_service.get_by_id(category_id=category_id)
        self.category_service.delete_category(category_dto=category_dto)
