import os
from typing import List

import requests
from dotenv import load_dotenv
from ninja import Router

from problems.models import Problem, TestCase
from .models import Solution
from .schemas import SolutionSchema, CodeSubmissionSchema, CodeSubmissionResultSchema

from users.authentication import jwt_auth

code_submission_router = Router(tags=["Code Submission"])

load_dotenv()

judge0_url = os.environ.get("JUDGE_URL").strip()


@code_submission_router.post("/submit_code", auth=jwt_auth, response={200: CodeSubmissionResultSchema, 400: dict})
def submit_code(request, payload: CodeSubmissionSchema):
    try:
        problem = Problem.objects.get(id=payload.problem_id)
        test_cases = TestCase.objects.filter(problem=problem)

        results = []
        passed_count = 0

        for test_case in test_cases:
            api_url = f"{judge0_url}/submissions?base64_encoded=false"
            headers = {"Content-Type": "application/json"}
            data = {
                "source_code": payload.source_code,
                "language_id": payload.language_id,
                "stdin": test_case.stdin
            }
            response = requests.post(api_url, json=data, headers=headers)
            token = response.json().get("token")

            if not token:
                return 400, {"error": "Failed to get token"}

            result_url = f"{judge0_url}/submissions/{token}?base64_encoded=false"
            status_id = 1
            while status_id in [1, 2]:
                result_response = requests.get(result_url, headers=headers)
                result_data = result_response.json()
                status_id = result_data.get("status", {}).get("id")
                if status_id in [1, 2]:
                    continue

            passed = result_data.get("stdout", "").strip() == test_case.expected_output.strip()
            if passed:
                passed_count += 1
            results.append({
                "test_case_id": test_case.id,
                "input": test_case.stdin,
                "expected_output": test_case.expected_output,
                "actual_output": result_data.get("stdout", ""),
                "status": result_data.get("status", {}).get("description", ""),
                "passed": passed
            })

        percentage_passed = int((passed_count / len(test_cases)) * 100) if test_cases else 0

        user = request.auth
        solution = Solution.objects.create(
            problem=problem,
            user=user,
            code=payload.source_code,
            language_id=payload.language_id,
            percentage_passed=percentage_passed
        )
        solution.save()

        return 200, {"results": results}

    except Problem.DoesNotExist:
        return 404, {"error": "Problem not found"}
    except Exception as e:
        return 400, {"error": str(e)}


@code_submission_router.get('/{user_id}/solutions', response=List[SolutionSchema])
def list_solutions(request, user_id: int):
    solutions = Solution.objects.filter(user_id=user_id)
    return [SolutionSchema.from_orm(solution) for solution in solutions]


@code_submission_router.get('/languages', response=List[dict])
def list_languages(request):
    api_url = f"{judge0_url}/languages"
    response = requests.get(api_url)
    return response.json()
