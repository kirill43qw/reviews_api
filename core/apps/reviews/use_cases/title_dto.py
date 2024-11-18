from dataclasses import dataclass

from core.apps.common.permission_service import PermissionService
from core.apps.customers.services.customers import BaseCustomersService
from core.apps.reviews.entities.titles import TitleEntity
from core.apps.reviews.services.search import BaseTitleSearchService
from core.apps.reviews.services.titles import BaseTitleService


@dataclass
class CreateTitleUseCase:
    customer_service: BaseCustomersService
    title_service: BaseTitleService
    elastic_service: BaseTitleSearchService
    permission_service: PermissionService

    def execute(self, token: str, title: TitleEntity):
        author = self.customer_service.get_by_token(token=token)
        self.permission_service.permission_only_admin(author=author)
        saved_title = self.title_service.create_title(title_data=title)
        self.elastic_service.upsert_title(title=saved_title)
        return saved_title


@dataclass
class UpdateTitleUseCase:
    customer_service: BaseCustomersService
    title_service: BaseTitleService
    elastic_service: BaseTitleSearchService
    permission_service: PermissionService

    def execute(
        self, token: str, title_id: int, title_data: TitleEntity
    ) -> TitleEntity:
        author = self.customer_service.get_by_token(token=token)
        self.permission_service.permission_only_admin(author=author)
        title = self.title_service.get_by_id(title_id=title_id)
        updated_title = self.title_service.update_title(
            title_dto=title, title_data=title_data
        )
        self.elastic_service.upsert_title(title=updated_title)
        return updated_title


@dataclass
class DeleteTitleUseCase:
    title_service: BaseTitleService
    elastic_service: BaseTitleSearchService
    customer_service: BaseCustomersService
    permission_service: PermissionService

    def execute(self, token: str, title_id: int):
        author = self.customer_service.get_by_token(token=token)
        self.permission_service.permission_only_admin(author=author)
        title = self.title_service.get_by_id(title_id=title_id)
        del_title = self.title_service.delete_title(title_dto=title)
        self.elastic_service.delete_title(title_id=title_id)
