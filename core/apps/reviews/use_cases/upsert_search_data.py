from dataclasses import dataclass

from core.apps.reviews.services.search import BaseTitleSearchService
from core.apps.reviews.services.titles import BaseTitleService


@dataclass
class UpsertSearchDataUseCase:
    search_service: BaseTitleSearchService
    title_service: BaseTitleService

    def execute(self):
        titles = self.title_service.get_all_title()

        for title in titles:
            self.search_service.upsert_title(title)
