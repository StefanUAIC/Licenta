import os
import requests
from ninja import Router
from .schemas import CodeSubmissionSchema
from dotenv import load_dotenv

code_submission_router = Router()

load_dotenv()

judge0_url = os.environ.get("JUDGE_URL").strip()


@code_submission_router.post("/submit/")
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

    return result_response.json()
