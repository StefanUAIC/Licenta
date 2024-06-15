from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router

from solutions.models import Solution
from solutions.schemas import SolutionSchema
from users.authentication import jwt_auth
from users.schemas import ProfileSchema
from .models import Class, Membership, User
from .schemas import ClassSchema
from .schemas import CreateClassSchema, JoinClassSchema, JoinClassResponseSchema

classes_router = Router(tags=["Classes"])


@classes_router.post('/create', auth=jwt_auth, response={201: ClassSchema, 400: dict})
def create_class(request, payload: CreateClassSchema):
    user = request.user
    if user.role != 'teacher':
        return 400, {"error": "Only teachers can create classes"}
    class_instance = Class.objects.create(name=payload.name, tag=payload.tag, teacher=user)
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


@classes_router.get('/{class_id}', auth=jwt_auth, response={200: ClassSchema, 400: dict})
def get_class_info(request, class_id: int):
    user = request.auth
    try:
        class_instance = Class.objects.get(id=class_id)
    except Class.DoesNotExist:
        return 400, {"error": "Class not found"}

    if not (Membership.objects.filter(student=user, class_instance=class_instance).exists()
            or class_instance.teacher == user):
        return 400, {"error": "You are not enrolled in this class"}

    return 200, ClassSchema.from_orm(class_instance)


@classes_router.delete('/{class_id}', auth=jwt_auth, response={204: None, 400: dict})
def delete_class(request, class_id: int):
    user = request.user
    class_instance = get_object_or_404(Class, id=class_id)
    if class_instance.teacher != user:
        return 400, {"error": "Only the teacher of the class can delete the class"}
    class_instance.delete()
    return 204, None


@classes_router.get('/{class_id}/students', auth=jwt_auth, response={200: List[ProfileSchema], 400: dict})
def list_class_students(request, class_id: int):
    user = request.user
    class_instance = get_object_or_404(Class, id=class_id)

    if user.role != 'teacher' and not Membership.objects.filter(student=user, class_instance=class_instance).exists():
        return 400, {"error": "You do not have permission to view the students of this class"}

    students = User.objects.filter(student_memberships__class_instance=class_instance)
    return 200, [ProfileSchema.from_orm(student) for student in students]
