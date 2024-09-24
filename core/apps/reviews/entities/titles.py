from dataclasses import dataclass, field
from datetime import datetime

from core.apps.common.enums import EntityStatus
from core.apps.reviews.entities import CategoryEntity, GenreEntity


@dataclass
class TitleEntity:
    # id: int
    title: str
    rating: int
    year: int
    description: str
    created_at: datetime
    updated_at: datetime
    id: int | None = field(default=None, kw_only=True)
    category: CategoryEntity | EntityStatus = field(default=EntityStatus.NOT_LOADED)
    genre: GenreEntity | EntityStatus = field(default=EntityStatus.NOT_LOADED)
