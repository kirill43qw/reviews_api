from dataclasses import dataclass


@dataclass(frozen=True)
class TitleFilters:
    search: str | None = None
