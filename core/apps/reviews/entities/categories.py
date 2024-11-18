from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CategoryEntity:
    title: str
    slug: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = field(default=None)
    id: int | None = field(default=None, kw_only=True)
