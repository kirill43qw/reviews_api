from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TitleEntity:
    title: str | None
    year: int | None
    description: str | None
    category_id: int | None
    rating: int | None = field(default=None)
    genre_ids: list[int] | None = field(default_factory=list)
    id: int | None = field(default=None, kw_only=True)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = field(default=None)
