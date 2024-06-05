from typing import List

from ninja import Router

from users.authentication import jwt_auth
from .models import Solution
from .schemas import SolutionSchema

solutions_router = Router(tags=["Solutions"])


@solutions_router.get('/{user_id}/', auth=jwt_auth, response=List[SolutionSchema])
def list_solutions(request, user_id: int):
    solutions = Solution.objects.filter(user_id=user_id)
    return [SolutionSchema.from_orm(solution) for solution in solutions]
