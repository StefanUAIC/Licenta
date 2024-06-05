from datetime import datetime
from typing import List

from ninja import Schema
from pydantic import field_validator


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
