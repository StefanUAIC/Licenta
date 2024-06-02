from typing import List

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from ninja import Router

from .models import Problem, TestCase
from .schemas import ProblemSchema, CreateProblemSchema, TestCaseSchema, CreateTestCaseSchema

problems_router = Router(tags=["Problems"])
User = get_user_model()


@problems_router.post('/create/', response={201: ProblemSchema, 400: dict})
def create_problem(request, payload: CreateProblemSchema):
    user = request.user
    problem = Problem.objects.create(
        title=payload.title,
        description=payload.description,
        difficulty=payload.difficulty,
        example_input=payload.example_input,
        example_output=payload.example_output,
        solution_code=payload.solution_code,
        created_by=user
    )
    return 201, ProblemSchema.from_orm(problem)


@problems_router.get('/{problem_id}/', response={200: ProblemSchema, 404: dict})
def get_problem(request, problem_id: int):
    problem = get_object_or_404(Problem, id=problem_id)
    return 200, ProblemSchema.from_orm(problem)


@problems_router.post('/{problem_id}/test_cases/', response={201: TestCaseSchema, 400: dict})
def create_test_case(request, problem_id: int, payload: CreateTestCaseSchema):
    problem = get_object_or_404(Problem, id=problem_id)
    test_case = TestCase.objects.create(
        problem=problem,
        stdin=payload.stdin,
        expected_output=payload.expected_output
    )
    return 201, TestCaseSchema.from_orm(test_case)


@problems_router.get('/{problem_id}/test_cases/', response=List[TestCaseSchema])
def list_test_cases(request, problem_id: int):
    test_cases = TestCase.objects.filter(problem_id=problem_id)
    return [TestCaseSchema.from_orm(test_case) for test_case in test_cases]
