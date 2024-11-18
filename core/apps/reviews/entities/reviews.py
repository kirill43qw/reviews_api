from dataclasses import dataclass, field
from datetime import datetime

from core.apps.common.enums import EntityStatus
from core.apps.reviews.entities import TitleEntity
from core.apps.customers.entities import CustomerEntity


@dataclass
class ReviewEntity:
    text: str
    rating: int
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = field(default=None)
    id: int | None = field(default=None, kw_only=True)
    author: CustomerEntity | EntityStatus = field(default=EntityStatus.NOT_LOADED)
    title: TitleEntity | EntityStatus = field(default=EntityStatus.NOT_LOADED)
