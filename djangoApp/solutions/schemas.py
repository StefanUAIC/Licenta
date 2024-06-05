from datetime import datetime

from ninja import Schema
from pydantic import field_validator


class SolutionSchema(Schema):
    id: int
    problem_id: int
    user_id: int
    code: str
    language_id: int
    created_at: str
    percentage_passed: int

    @field_validator('created_at', mode='before')
    def format_datetime(cls, value: datetime) -> str:
        if isinstance(value, datetime):
            return value.isoformat()
        return value
