from dataclasses import dataclass

# from ninja import Schema


# class CategoryFilters(Schema):
#     search: str | None = None


@dataclass(frozen=True)
class CategoryFilters:
    search: str | None = None
