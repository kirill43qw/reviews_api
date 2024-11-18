from datetime import datetime
from dataclasses import dataclass, field

from core.apps.common.enums import EntityStatus
from core.apps.customers.entities import CustomerEntity
from core.apps.reviews.entities.reviews import ReviewEntity


@dataclass
class CommentEntity:
    text: str
    author: CustomerEntity | EntityStatus = field(default=EntityStatus.NOT_LOADED)
    review: ReviewEntity | EntityStatus = field(default=EntityStatus.NOT_LOADED)
    id: int | None = field(default=None, kw_only=True)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = field(default=None)
