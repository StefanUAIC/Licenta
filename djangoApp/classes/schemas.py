import uuid
from datetime import datetime

from ninja import Schema
from pydantic import BaseModel, field_validator


class ClassSchema(Schema):
    id: int
    name: str
    teacher_id: int
    created_at: str
    join_code: str

    @field_validator('created_at', mode='before')
    def format_created_at(cls, value: datetime) -> str:
        if isinstance(value, datetime):
            return value.isoformat()
        return value

    @field_validator('join_code', mode='before')
    def format_join_code(cls, value: uuid.UUID) -> str:
        if isinstance(value, uuid.UUID):
            return str(value)
        return value


class MembershipSchema(Schema):
    id: int
    student_id: int
    class_instance_id: int


class HomeworkSchema(Schema):
    id: int
    class_instance_id: int
    problem_id: int
    due_date: str


class CreateClassSchema(Schema):
    name: str


class CreateHomeworkSchema(Schema):
    problem_id: int
    due_date: str


class JoinClassSchema(Schema):
    join_code: str


class JoinClassResponseSchema(Schema):
    class_id: int
    name: str


class ClassResponseSchema(Schema):
    id: int
    name: str
    teacher_id: int


class ErrorResponseSchema(Schema):
    error: str
