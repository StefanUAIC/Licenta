from ninja import Schema
from pydantic import BaseModel


class ClassSchema(Schema):
    id: int
    name: str
    teacher_id: int
    created_at: str
    join_code: str


class MembershipSchema(Schema):
    id: int
    student_id: int
    class_instance_id: int


class HomeworkSchema(Schema):
    id: int
    class_instance_id: int
    problem_id: int
    due_date: str


class CreateClassSchema(BaseModel):
    name: str


class CreateHomeworkSchema(BaseModel):
    problem_id: int
    due_date: str


class JoinClassSchema(BaseModel):
    join_code: str
