from dataclasses import dataclass, field
from datetime import datetime

from core.apps.common.enums import EntityStatus
from core.apps.reviews.entities import TitleEntity
from core.apps.customers.entities import CustomerEntity


@dataclass
class ReviewEntity:
    # id: int
    text: str
    rating: int
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = field(default=None)
    id: int | None = field(default=None, kw_only=True)
    author: CustomerEntity | EntityStatus = field(default=EntityStatus.NOT_LOADED)
    title: TitleEntity | EntityStatus = field(default=EntityStatus.NOT_LOADED)


# @dataclass
# class ReviewEntity:
#     id: int | None = field(default=None, kw_only=True)  # noqa
#     customer: CustomerEntity | EntityStatus = field(default=EntityStatus.NOT_LOADED)
#     title: TitleEntity | EntityStatus = field(default=EntityStatus.NOT_LOADED)
#
#     text: str = field(default="")
#     rating: int = field(default=1)
#
#     created_at: datetime = field(default_factory=datetime.utcnow)
#     updated_at: datetime | None = field(default=None)
