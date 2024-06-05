from .models import Solution


def create_solution(user, problem, source_code, language_id, percentage_passed):
    solution = Solution.objects.create(
        problem=problem,
        user=user,
        code=source_code,
        language_id=language_id,
        percentage_passed=percentage_passed
    )
    solution.save()
    return solution
