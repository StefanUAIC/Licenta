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
    memory_exceeded: bool
    time_exceeded: bool
    compile_output: Optional[str] = None
    stderr: Optional[str] = None
    message: Optional[str] = None


class CodeSubmissionResultSchema(Schema):
    results: List[TestCaseResultSchema]


class TestCaseVerifySchema(Schema):
    id: int = 0
    stdin: str
    expected_output: str


class VerifyCodeSubmissionSchema(Schema):
    source_code: str
    language_id: int
    test_cases: List[TestCaseVerifySchema]
    memory_limit: int
    time_limit: int


class TestCaseVerifyResultSchema(Schema):
    test_case_id: int
    input: str
    expected_output: str
    actual_output: str
    status: str
    passed: bool
    memory_exceeded: bool
    time_exceeded: bool


class VerifyCodeSubmissionResultSchema(Schema):
    results: List[TestCaseVerifyResultSchema]
