from pydantic import BaseModel


class CodeSubmissionSchema(BaseModel):
    source_code: str
    language_id: int = 71
    stdin: str = ""
