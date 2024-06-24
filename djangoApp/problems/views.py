from typing import List

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from ninja import Router

from users.authentication import jwt_auth
from .models import Problem, TestCase
from .schemas import ProblemSchema, CreateProblemSchema, TestCaseSchema, CreateTestCaseSchema

problems_router = Router(tags=["Problems"])
User = get_user_model()


@problems_router.get('/', auth=jwt_auth, response=List[ProblemSchema])
def list_problems(request):
    if not request.user.is_authenticated:
        print("User is not authenticated")
    problems = Problem.objects.filter(status='ACCEPTED')
    return [ProblemSchema.from_orm(problem) for problem in problems]


@problems_router.post('/', auth=jwt_auth, response={201: ProblemSchema, 400: dict})
def create_problem(request, payload: CreateProblemSchema):
    user = request.auth
    problem = Problem.objects.create(
        title=payload.title,
        description=payload.description,
        difficulty=payload.difficulty,
        example_input=payload.example_input,
        example_output=payload.example_output,
        solution_code=payload.solution_code,
        created_by=user,
        grade=payload.grade,
        category=payload.category,
        memory_limit=payload.memory_limit,
        time_limit=payload.time_limit
    )
    return 201, ProblemSchema.from_orm(problem)


@problems_router.get('/{problem_id}/', auth=jwt_auth, response={200: ProblemSchema, 404: dict})
def get_problem(request, problem_id: int):
    problem = get_object_or_404(Problem, id=problem_id, status='ACCEPTED')
    return 200, ProblemSchema.from_orm(problem)


@problems_router.post('/{problem_id}/test_cases/', auth=jwt_auth, response={201: TestCaseSchema, 400: dict})
def create_test_case(request, problem_id: int, payload: CreateTestCaseSchema):
    problem = get_object_or_404(Problem, id=problem_id)
    if problem.id != problem_id:
        return 400, {"error": "Problem not found"}

    test_case = TestCase.objects.create(
        problem_id=problem_id,
        stdin=payload.stdin,
        expected_output=payload.expected_output
    )
    return 201, TestCaseSchema.from_orm(test_case)


@problems_router.get('/{problem_id}/test_cases/', response=List[TestCaseSchema])
def list_test_cases(request, problem_id: int):
    test_cases = TestCase.objects.filter(problem_id=problem_id)
    return [TestCaseSchema.from_orm(test_case) for test_case in test_cases]
