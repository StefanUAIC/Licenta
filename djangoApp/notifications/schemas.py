from datetime import datetime

from ninja import Schema
from pydantic import field_validator


class NotificationSchema(Schema):
    id: int
    message: str
    created_at: str
    is_read: bool

    @field_validator('created_at', mode='before')
    def format_created_at(cls, value: datetime) -> str:
        if isinstance(value, datetime):
            return value.isoformat()
        return value
