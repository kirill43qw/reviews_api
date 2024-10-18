from typing import Any

from django.core.management import BaseCommand

from core.apps.common.containers import get_container
from core.apps.reviews.use_cases.upsert_search_data import UpsertSearchDataUseCase


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        container = get_container()

        use_case: UpsertSearchDataUseCase = container.resolve(UpsertSearchDataUseCase)
        use_case.execute()
