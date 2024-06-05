from datetime import datetime
from typing import List

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


class CreateSolutionSchema(Schema):
    problem_id: int
    code: str
    language_id: int = 71


class CodeSubmissionSchema(Schema):
    source_code: str
    language_id: int
    problem_id: int


class TestCaseResultSchema(Schema):
    test_case_id: int
    input: str
    expected_output: str
    actual_output: str
    status: str
    passed: bool


class CodeSubmissionResultSchema(Schema):
    results: List[TestCaseResultSchema]
