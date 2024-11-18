from ninja import Schema


class UserFilter(Schema):
    search: str | None = None
