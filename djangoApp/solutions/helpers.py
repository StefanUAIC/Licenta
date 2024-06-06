from .models import Solution


def create_solution(user, problem, source_code, language_id, percentage_passed):
    print("create_solution")
    solution = Solution.objects.create(
        problem=problem,
        user=user,
        code=source_code,
        language_id=language_id,
        percentage_passed=percentage_passed
    )
    solution.save()
