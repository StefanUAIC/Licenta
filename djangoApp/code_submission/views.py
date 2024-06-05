import os
from typing import List

import requests
from dotenv import load_dotenv
from ninja import Router

from .models import Solution
from .schemas import SolutionSchema, CodeSubmissionSchema

code_submission_router = Router(tags=["Code Submission"])

load_dotenv()

judge0_url = os.environ.get("JUDGE_URL").strip()


@code_submission_router.post("/submit_code", response={200: SolutionSchema, 400: dict, 404: dict})
def submit_code(request, payload: CodeSubmissionSchema):
    api_url = f"{judge0_url}/submissions?base64_encoded=false"
    headers = {"Content-Type": "application/json"}
    data = {
        "source_code": payload.source_code,
        "language_id": payload.language_id,
        "stdin": payload.stdin
    }
    response = requests.post(api_url, json=data, headers=headers)
    token = response.json().get("token")

    if not token:
        return {"error": "Failed to get token"}

    result_url = f"{judge0_url}/submissions/{token}?base64_encoded=false"
    result_response = requests.get(result_url, headers=headers)

    while result_response.json().get("status").get("id") in [1, 2]:
        result_response = requests.get(result_url, headers=headers)

    return SolutionSchema()


# @code_submission_router.post('/submit_solution/', response={200: SolutionSchema, 400: dict, 404: dict})
# def submit_solution(request, payload: CreateSolutionSchema):
#     problem = get_object_or_404(Problem, id=payload.problem_id)
#     user = request.user
#
#     test_cases = TestCase.objects.filter(problem=problem)
#
#     for test_case in test_cases:
#         api_url = f"{judge0_url}/submissions?base64_encoded=false"
#         headers = {"Content-Type": "application/json"}
#         data = {
#             "source_code": payload.code,
#             "language_id": payload.language_id,
#             "stdin": test_case.stdin
#         }
#         response = requests.post(api_url, json=data, headers=headers)
#         token = response.json().get("token")
#
#         if not token:
#             return {"error": "Failed to get token"}
#
#         result_url = f"{judge0_url}/submissions/{token}?base64_encoded=false"
#         result_response = requests.get(result_url, headers=headers)
#
#         while result_response.json().get("status").get("id") in [1, 2]:
#             result_response = requests.get(result_url, headers=headers)
#
#         if result_response.json().get("stdout") != test_case.expected_output:
#             return {"error": "Test case failed", "details": result_response.json()}
#
#     # Save the solution
#     solution = Solution.objects.create(
#         problem=problem,
#         user=user,
#         code=payload.code,
#         language_id=payload.language_id
#     )
#
#     return 200, SolutionSchema.from_orm(solution)


@code_submission_router.get('/{problem_id}/solutions', response=List[SolutionSchema])
def list_solutions(request, problem_id: int):
    solutions = Solution.objects.filter(problem_id=problem_id)
    return [SolutionSchema.from_orm(solution) for solution in solutions]


@code_submission_router.get('/languages', response=List[dict])
def list_languages(request):
    api_url = f"{judge0_url}/languages"
    response = requests.get(api_url)
    return response.json()
