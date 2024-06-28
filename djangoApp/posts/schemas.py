from datetime import datetime

from ninja import Schema
from pydantic import field_validator


class PostSchema(Schema):
    title: str
    content: str


class PostOutSchema(Schema):
    id: int
    title: str
    content: str
    author: str
    created_at: str
    author_id: int

    @field_validator('created_at', mode='before')
    def format_created_at(cls, value: datetime) -> str:
        if isinstance(value, datetime):
            return value.isoformat()
        return value
