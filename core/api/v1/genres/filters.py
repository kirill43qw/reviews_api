from ninja import Schema


class GenreFilters(Schema):
    search: str | None = None
