from ninja import Schema
from pydantic import BaseModel


class SolutionSchema(Schema):
    id: int
    problem_id: int
    user_id: int
    code: str
    language_id: int
    created_at: str
    updated_at: str


class CreateSolutionSchema(BaseModel):
    problem_id: int
    code: str
    language_id: int = 71


class CodeSubmissionSchema(BaseModel):
    source_code: str
    language_id: int = 71
    stdin: str = ""
