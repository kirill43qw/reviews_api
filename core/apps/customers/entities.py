from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CustomerEntity:
    username: str | None
    phone: str | None
    bio: str | None
    role: str | None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = field(default=None)
    id: int | None = field(default=None, kw_only=True)

    @property
    def is_moderator(self) -> bool:
        return self.role == "moderator"

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"
