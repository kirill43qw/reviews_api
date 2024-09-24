from dataclasses import dataclass
from datetime import datetime


@dataclass
class CategoryEntity:
    id: int
    title: str
    slug: str
    created_at: datetime
    updated_at: datetime
