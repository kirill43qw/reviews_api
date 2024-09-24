from ninja import Schema


class CategoryFilters(Schema):
    search: str | None = None
