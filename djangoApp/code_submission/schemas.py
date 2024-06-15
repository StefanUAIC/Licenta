from typing import List, Optional

from ninja import Schema


class CodeSubmissionSchema(Schema):
    source_code: str
    language_id: int
    problem_id: int
    homework_id: Optional[int] = None


class TestCaseResultSchema(Schema):
    test_case_id: int
    input: str
    expected_output: str
    actual_output: str
    status: str
    passed: bool


class CodeSubmissionResultSchema(Schema):
    results: List[TestCaseResultSchema]
