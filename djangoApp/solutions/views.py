from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from .models import Solution
from .schemas import SolutionSchema

solutions_router = Router(tags=["Solutions"])


@solutions_router.get('/{problem_id}/', response=List[SolutionSchema])
def list_solutions(request, problem_id: int):
    solutions = Solution.objects.filter(problem_id=problem_id)
    return [SolutionSchema.from_orm(solution) for solution in solutions]
