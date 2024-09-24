from dataclasses import dataclass


@dataclass(frozen=True)
class GenreFilters:
    search: str | None = None
