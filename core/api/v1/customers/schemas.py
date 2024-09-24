from ninja import Schema


class AuthInSchema(Schema):
    username: str
    phone: str


class AuthOutSchema(Schema):
    message: str


class TokenOutSchema(Schema):
    token: str


class TokenInSchema(Schema):
    phone: str
    code: str
