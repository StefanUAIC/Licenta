from datetime import datetime
from typing import List

from ninja import Router

from problems.models import Problem
from solutions.models import Solution
from solutions.schemas import SolutionSchema
from users.authentication import jwt_auth
from .models import Class, Membership, Homework
from .schemas import ClassResponseSchema, ErrorResponseSchema
from .schemas import ClassSchema, HomeworkSchema
from .schemas import CreateClassSchema, CreateHomeworkSchema
from .schemas import JoinClassSchema, JoinClassResponseSchema

classes_router = Router(tags=["Classes"])


@classes_router.post('/create', auth=jwt_auth, response={201: ClassSchema, 400: dict})
def create_class(request, payload: CreateClassSchema):
    user = request.user
    if user.role != 'teacher':
        return 400, {"error": "Only teachers can create classes"}
    class_instance = Class.objects.create(name=payload.name, teacher=user)
    return 201, ClassSchema.from_orm(class_instance)


@classes_router.post('/join', auth=jwt_auth, response={201: JoinClassResponseSchema, 400: dict})
def join_class(request, payload: JoinClassSchema):
    user = request.user
    class_instance = Class.objects.filter(join_code=payload.join_code).first()
    if not class_instance:
        return 400, {"error": "Invalid join code"}
    if Membership.objects.filter(student=user, class_instance=class_instance).exists():
        return 400, {"error": "You are already enrolled in this class"}
    Membership.objects.create(student=user, class_instance=class_instance)
    return 201, JoinClassResponseSchema(class_id=class_instance.id, name=class_instance.name)


@classes_router.post('/{class_id}/add_homework', auth=jwt_auth, response={201: HomeworkSchema, 400: dict})
def add_homework(request, class_id: int, payload: CreateHomeworkSchema):
    user = request.user
    class_instance = Class.objects.get(id=class_id)
    if class_instance.teacher != user:
        return 400, {"error": "Only the teacher of the class can add homework"}
    problem = Problem.objects.get(id=payload.problem_id)
    homework = Homework.objects.create(class_instance=class_instance, problem=problem, due_date=payload.due_date)
    return 201, HomeworkSchema.from_orm(homework)


@classes_router.get('/{class_id}/submissions', auth=jwt_auth, response=List[SolutionSchema])
def list_submissions(request, class_id: int):
    user = request.user
    class_instance = Class.objects.get(id=class_id)
    if user.role == 'teacher' and class_instance.teacher == user:
        submissions = Solution.objects.filter(problem__homeworks__class_instance_id=class_id)
        return [SolutionSchema.from_orm(submission) for submission in submissions]
    return 400, {"error": "Only the teacher of the class can view submissions"}


@classes_router.post('/{homework_id}/submit', auth=jwt_auth, response={201: SolutionSchema, 400: dict})
def submit_homework(request, homework_id: int, payload: SolutionSchema):
    user = request.user
    homework = Homework.objects.get(id=homework_id)
    if not Membership.objects.filter(student=user, class_instance=homework.class_instance).exists():
        return 400, {"error": "Only students enrolled in the class can submit homework"}
    solution = Solution.objects.create(
        problem=homework.problem,
        user=user,
        code=payload.code,
        language_id=payload.language_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    return 201, SolutionSchema.from_orm(solution)


@classes_router.get('/{class_id}', auth=jwt_auth, response={200: ClassSchema, 400: dict})
def get_class_info(request, class_id: int):
    user = request.auth
    try:
        class_instance = Class.objects.get(id=class_id)
    except Class.DoesNotExist:
        return 400, {"error": "Class not found"}

    if not Membership.objects.filter(student=user, class_instance=class_instance).exists():
        return 400, {"error": "You are not enrolled in this class"}

    return 200, ClassSchema.from_orm(class_instance)
