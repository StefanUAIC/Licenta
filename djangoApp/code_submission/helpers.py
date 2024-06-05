import os

import requests
from dotenv import load_dotenv

load_dotenv()

judge0_url = os.environ.get("JUDGE_URL").strip()


def submit_and_test_code(source_code, language_id, test_cases):
    results = []
    passed_count = 0

    for test_case in test_cases:
        api_url = f"{judge0_url}/submissions?base64_encoded=false"
        headers = {"Content-Type": "application/json"}
        data = {
            "source_code": source_code,
            "language_id": language_id,
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
            print("result_data1111", result_data)
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
            "passed": passed,
            "compile_output": result_data.get("compile_output", ""),
            "stderr": result_data.get("stderr", ""),
            "message": result_data.get("message", "")
        })

    return 200, {"results": results, "passed_count": passed_count, "total_count": len(test_cases)}
