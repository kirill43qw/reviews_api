from ninja import Schema


class TitleFilters(Schema):
    search: str | None = None
