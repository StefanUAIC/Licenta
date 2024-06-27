from datetime import datetime, timezone

from ninja import Schema
from pydantic import field_validator


class HomeworkSchema(Schema):
    id: int
    class_instance_id: int
    problem_id: int
    due_date: str

    @field_validator('due_date', mode='before')
    def format_due_date(cls, value: datetime) -> str:
        if isinstance(value, datetime):
            return value.isoformat()
        return value


class CreateHomeworkSchema(Schema):
    problem_id: int
    class_instance_id: int
    due_date: str

    @field_validator('due_date', mode='before')
    def validate_due_date(cls, value) -> str:
        if not isinstance(value, str):
            value = str(value)

        parsed_date = datetime.fromisoformat(value)

        if parsed_date.tzinfo is None:
            parsed_date = parsed_date.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)

        if parsed_date <= now:
            raise ValueError('Due date must be in the future')

        return value


class HomeworkDetailSchema(Schema):
    id: int
    class_instance_id: int
    problem_id: int
    due_date: str
    class_instance_name: str
    problem_title: str

    @field_validator('due_date', mode='before')
    def format_due_date(cls, value: datetime) -> str:
        if isinstance(value, datetime):
            return value.isoformat()
        return value
