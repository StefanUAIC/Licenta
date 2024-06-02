from ninja import Schema


class ProblemSchema(Schema):
    id: int
    title: str
    description: str
    difficulty: str
    example_input: str
    example_output: str
    created_at: str
    updated_at: str
    created_by: str


class CreateProblemSchema(Schema):
    title: str
    description: str
    difficulty: str
    example_input: str
    example_output: str
    solution_code: str


class TestCaseSchema(Schema):
    id: int
    problem_id: int
    stdin: str
    expected_output: str


class CreateTestCaseSchema(Schema):
    problem_id: int
    stdin: str
    expected_output: str
