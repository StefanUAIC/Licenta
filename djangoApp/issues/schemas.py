from datetime import datetime

from ninja import Schema
from pydantic import constr, field_validator


class IssuesSchema(Schema):
    title: constr(min_length=3, max_length=255)
    description: constr(min_length=5)


class IssuesResponseSchema(Schema):
    id: int
    title: str
    description: str
    created_at: str

    @field_validator('created_at', mode='before')
    def format_created_at(cls, value: datetime) -> str:
        if isinstance(value, datetime):
            return value.isoformat()
        return value
