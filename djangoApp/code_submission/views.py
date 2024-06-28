import os
from typing import List

import requests
from dotenv import load_dotenv
from ninja import Router

from homeworks.models import Homework
from problems.models import Problem, TestCase
from solutions.helpers import create_solution
from users.authentication import jwt_auth
from .helpers import submit_and_test_code
from .schemas import CodeSubmissionSchema, CodeSubmissionResultSchema, TestCaseVerifySchema, VerifyCodeSubmissionSchema, \
    VerifyCodeSubmissionResultSchema, TestCaseResultSchema, TestCaseVerifyResultSchema

code_submission_router = Router(tags=["Code Submission"])

load_dotenv()

judge0_url = os.environ.get("JUDGE_URL").strip()


@code_submission_router.post("/submit_code", auth=jwt_auth,
                             response={200: CodeSubmissionResultSchema, 400: dict, 404: dict})
def submit_code(request, payload: CodeSubmissionSchema):
    try:
        problem = Problem.objects.get(id=payload.problem_id)
        test_cases = TestCase.objects.filter(problem=problem)

        status, result_data = submit_and_test_code(
            payload.source_code,
            payload.language_id,
            test_cases,
            problem.memory_limit,
            problem.time_limit
        )

        if status != 200:
            return status, result_data

        raw_results = result_data["results"]
        passed_count = result_data["passed_count"]
        total_count = result_data["total_count"]

        percentage_passed = int((passed_count / total_count) * 100) if total_count else 0

        user = request.auth
        homework = None
        if payload.homework_id:
            homework = Homework.objects.get(id=payload.homework_id)

        create_solution(user, problem, payload.source_code, payload.language_id, percentage_passed, homework)

        formatted_results = [
            TestCaseResultSchema(
                test_case_id=result['test_case_id'],
                input=result['input'],
                expected_output=result['expected_output'],
                actual_output=result['actual_output'],
                status=result['status'],
                passed=result['passed'],
                memory_exceeded=result['memory_exceeded'],
                time_exceeded=result['time_exceeded'],
                compile_output=result['compile_output'],
                stderr=result['stderr'],
                message=result['message']
            ) for result in raw_results
        ]

        return 200, CodeSubmissionResultSchema(results=formatted_results)

    except Problem.DoesNotExist:
        return 404, {"error": "Problem not found"}
    except Exception as e:
        return 400, {"error": str(e)}


@code_submission_router.post("/", auth=jwt_auth, response={200: CodeSubmissionResultSchema, 400: dict})
def test_code(request, payload: CodeSubmissionSchema):
    try:
        problem = Problem.objects.get(id=payload.problem_id)
        test_cases = TestCase.objects.filter(problem=problem)

        status, result_data = submit_and_test_code(payload.source_code, payload.language_id, test_cases,
                                                   problem.memory_limit, problem.time_limit)

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


@code_submission_router.post("/verify_test_cases", auth=jwt_auth,
                             response={200: VerifyCodeSubmissionResultSchema, 400: dict})
def verify_test_cases(request, payload: VerifyCodeSubmissionSchema):
    try:
        test_cases = []
        for i, tc in enumerate(payload.test_cases):
            test_cases.append(TestCaseVerifySchema(
                id=tc.id if tc.id is not None else i,
                stdin=tc.stdin,
                expected_output=tc.expected_output
            ))

        status, result_data = submit_and_test_code(
            payload.source_code,
            payload.language_id,
            test_cases,
            payload.memory_limit,
            payload.time_limit
        )

        if status != 200:
            return status, result_data

        verified_results = [
            TestCaseVerifyResultSchema(
                test_case_id=result['test_case_id'],
                input=result['input'],
                expected_output=result['expected_output'],
                actual_output=result['actual_output'],
                status=result['status'],
                passed=result['passed'],
                memory_exceeded=result['memory_exceeded'],
                time_exceeded=result['time_exceeded']
            )
            for result in result_data["results"]
        ]
        response = VerifyCodeSubmissionResultSchema(results=verified_results)
        return 200, response

    except Exception as e:
        return 400, {"error": str(e)}
