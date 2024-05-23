from ninja import Schema


class UserSchema(Schema):
    username: str
    password: str
    role: str
    email: str
    first_name: str
    last_name: str


class TokenSchema(Schema):
    token: str
    user_id: int
    username: str
    role: str
    email: str
    first_name: str
    last_name: str
