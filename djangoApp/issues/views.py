from ninja import Router

from users.authentication import jwt_auth
from .models import Issue
from .schemas import IssuesSchema, IssuesResponseSchema

issues_router = Router(tags=["Issues"])


@issues_router.post("/", auth=jwt_auth, response={201: IssuesResponseSchema, 400: dict})
def create_issue(request, payload: IssuesSchema):
    issue = Issue.objects.create(
        title=payload.title,
        description=payload.description,
        author=request.auth
    )
    return 201, issue
