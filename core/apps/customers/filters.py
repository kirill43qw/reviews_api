from dataclasses import dataclass


@dataclass(frozen=True)
class UserFilters:
    search: str | None = None
