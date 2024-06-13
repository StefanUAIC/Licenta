from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router

from classes.models import Class, Membership
from problems.models import Problem
from users.authentication import jwt_auth
from .models import Homework
from .schemas import HomeworkDetailSchema
from .schemas import HomeworkSchema, CreateHomeworkSchema

homework_router = Router(tags=["Homework"])


@homework_router.post('/', auth=jwt_auth, response={201: HomeworkSchema, 400: dict})
def create_homework(request, payload: CreateHomeworkSchema):
    user = request.user
    class_instance = get_object_or_404(Class, id=payload.class_instance_id)
    if class_instance.teacher != user:
        return 400, {"error": "Only the teacher of the class can add homework"}
    problem = get_object_or_404(Problem, id=payload.problem_id)
    homework = Homework.objects.create(
        class_instance=class_instance,
        problem=problem,
        due_date=payload.due_date
    )
    return 201, HomeworkSchema.from_orm(homework)


@homework_router.get('/{homework_id}', auth=jwt_auth, response={200: HomeworkDetailSchema, 400: dict})
def get_homework(request, homework_id: int):
    user = request.user
    homework = get_object_or_404(Homework, id=homework_id)
    class_instance = homework.class_instance

    if class_instance.teacher != user and not Membership.objects.filter(student=user,
                                                                        class_instance=class_instance).exists():
        return 400, {"error": "You do not have permission to view this homework"}

    homework_detail = HomeworkDetailSchema(
        id=homework.id,
        class_instance_id=class_instance.id,
        problem_id=homework.problem.id,
        due_date=homework.due_date.isoformat(),
        class_instance_name=class_instance.name,
        problem_title=homework.problem.title
    )
    return 200, homework_detail


@homework_router.delete('/{homework_id}', auth=jwt_auth, response={204: None, 400: dict})
def delete_homework(request, homework_id: int):
    user = request.user
    homework = get_object_or_404(Homework, id=homework_id)
    if homework.class_instance.teacher != user:
        return 400, {"error": "Only the teacher of the class can delete the homework"}
    homework.delete()
    return 204, None


@homework_router.get('/class/{class_id}', auth=jwt_auth, response={200: List[HomeworkSchema], 400: dict})
def get_class_homeworks(request, class_id: int):
    user = request.user
    class_instance = get_object_or_404(Class, id=class_id)

    if class_instance.teacher != user and not Membership.objects.filter(student=user,
                                                                        class_instance=class_instance).exists():
        return 400, {"error": "You do not have permission to view this class's homeworks"}

    homeworks = Homework.objects.filter(class_instance=class_instance)
    return 200, [HomeworkSchema.from_orm(homework) for homework in homeworks]
