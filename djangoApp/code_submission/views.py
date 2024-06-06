import os
from typing import List

import requests
from dotenv import load_dotenv
from ninja import Router

from problems.models import Problem, TestCase
from solutions.helpers import create_solution
from users.authentication import jwt_auth
from .helpers import submit_and_test_code
from .schemas import CodeSubmissionSchema, CodeSubmissionResultSchema

code_submission_router = Router(tags=["Code Submission"])

load_dotenv()

judge0_url = os.environ.get("JUDGE_URL").strip()


@code_submission_router.post("/submit_code", auth=jwt_auth, response={200: CodeSubmissionResultSchema, 400: dict})
def submit_code(request, payload: CodeSubmissionSchema):
    try:
        print(payload)
        problem = Problem.objects.get(id=payload.problem_id)
        test_cases = TestCase.objects.filter(problem=problem)

        status, result_data = submit_and_test_code(payload.source_code, payload.language_id, test_cases)
        print("result_data", result_data)
        print("status", status)
        if status != 200:
            return status, result_data

        results = result_data["results"]
        passed_count = result_data["passed_count"]
        total_count = result_data["total_count"]

        percentage_passed = int((passed_count / total_count) * 100) if total_count else 0

        user = request.auth
        create_solution(user, problem, payload.source_code, payload.language_id, percentage_passed)

        return 200, {"results": results}

    except Problem.DoesNotExist:
        return 404, {"error": "Problem not found"}
    except Exception as e:
        return 400, {"error": str(e)}


@code_submission_router.post("/", auth=jwt_auth, response={200: CodeSubmissionResultSchema, 400: dict})
def test_code(request, payload: CodeSubmissionSchema):
    try:
        problem = Problem.objects.get(id=payload.problem_id)
        test_cases = TestCase.objects.filter(problem=problem)

        status, result_data = submit_and_test_code(payload.source_code, payload.language_id, test_cases)

        return status, result_data

    except Problem.DoesNotExist:
        return 404, {"error": "Problem not found"}
    except Exception as e:
        return 400, {"error": str(e)}


@code_submission_router.get('/languages', response=List[dict])
def list_languages(request):
    api_url = f"{judge0_url}/languages"
    response = requests.get(api_url)
    return response.json()
