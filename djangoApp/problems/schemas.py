from datetime import datetime

from django.contrib.auth import get_user_model
from ninja import Schema
from pydantic import field_validator

User = get_user_model()


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
    grade: int
    category: str

    @field_validator('created_at', 'updated_at', mode='before')
    def format_datetime(cls, value: datetime) -> str:
        if isinstance(value, datetime):
            return value.isoformat()
        return value

    @field_validator('created_by', mode='before')
    def format_created_by(cls, value: User) -> str:
        if isinstance(value, User):
            return value.username
        return value


class CreateProblemSchema(Schema):
    title: str
    description: str
    difficulty: str
    example_input: str
    example_output: str
    solution_code: str
    grade: int
    category: str

    @field_validator('difficulty')
    def validate_difficulty(cls, value):
        valid_difficulties = ['easy', 'medium', 'hard']
        if value not in valid_difficulties:
            raise ValueError(f'difficulty must be one of {valid_difficulties}')
        return value

    @field_validator('grade')
    def validate_grade(cls, value):
        valid_grades = [9, 10, 11, 12]
        if value not in valid_grades:
            raise ValueError(f'grade must be one of {valid_grades}')
        return value

    @field_validator('category')
    def validate_category(cls, value):
        valid_categories = [
            'arrays', 'linked_lists', 'sorting', 'searching', 'trees', 'graphs',
            'dynamic_programming', 'recursion', 'backtracking', 'bit_manipulation',
            'greedy', 'math', 'geometry', 'combinatorics', 'probability',
            'game_theory', 'puzzles', 'miscellaneous'
        ]
        if value not in valid_categories:
            raise ValueError(f'category must be one of {valid_categories}')
        return value


class TestCaseSchema(Schema):
    id: int
    problem_id: int
    stdin: str
    expected_output: str


class CreateTestCaseSchema(Schema):
    problem_id: int
    stdin: str
    expected_output: str
