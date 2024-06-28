import os

import requests
from dotenv import load_dotenv

load_dotenv()

judge0_url = os.environ.get("JUDGE_URL").strip()


def submit_and_test_code(source_code, language_id, test_cases, memory_limit, time_limit):
    results = []
    passed_count = 0

    for test_case in test_cases:
        passed = False
        api_url = f"{judge0_url}/submissions?base64_encoded=false"
        headers = {"Content-Type": "application/json"}
        data = {
            "source_code": source_code,
            "language_id": language_id,
            "stdin": test_case.stdin,
            "cpu_time_limit": time_limit,
            "cpu_extra_time": 1,
            "wall_time_limit": 20.0,
        }
        response = requests.post(api_url, json=data, headers=headers)
        print(response.json())
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

        print(result_data)
        memory_exceeded = result_data.get("memory", 0) > memory_limit
        time_exceeded = float(result_data.get("time", 0)) > time_limit

        if result_data.get("stdout") is None:
            result_data["stdout"] = ""
        passed = (result_data.get("stdout", "").strip() == test_case.expected_output.strip()
                  and not (memory_exceeded or time_exceeded))

        if memory_exceeded:
            result_data["status"]["description"] = "Memory Limit Exceeded"
        elif time_exceeded:
            result_data["status"]["description"] = "Time Limit Exceeded"

        if passed:
            passed_count += 1

        results.append({
            "test_case_id": test_case.id,
            "input": test_case.stdin,
            "expected_output": test_case.expected_output,
            "actual_output": result_data.get("stdout", ""),
            "status": result_data.get("status", {}).get("description", ""),
            "passed": passed,
            "memory_exceeded": memory_exceeded,
            "time_exceeded": time_exceeded,
            "compile_output": result_data.get("compile_output", ""),
            "stderr": result_data.get("stderr", ""),
            "message": result_data.get("message", "")
        })

    return 200, {"results": results, "passed_count": passed_count, "total_count": len(test_cases)}
