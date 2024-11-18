from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class GenreEntity:
    title: str
    slug: str
    id: int | None = field(default=None, kw_only=True)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = field(default=None)
