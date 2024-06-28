import base64
from typing import List, Literal

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from ninja import Router
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken

from classes.models import Class
from classes.schemas import ClassResponseSchema
from problems.schemas import ProblemSchema
from solutions.models import Solution
from solutions.schemas import SolutionSchema
from .authentication import jwt_auth
from .schemas import ErrorResponseSchema, ErrorDetailSchema, UpdateProfileSchema
from .schemas import ProfileSchema, RoleResponseSchema
from .schemas import TokenRefreshSchema, RefreshTokenSchema
from .schemas import UserSchema, TokenSchema, LoginSchema

User = get_user_model()

user_router = Router(tags=["Users"])


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@user_router.post('/register', response={200: TokenSchema, 409: ErrorResponseSchema, 500: ErrorResponseSchema})
def register(request, user_in: UserSchema):
    try:
        with transaction.atomic():
            errors = []
            if User.objects.filter(username=user_in.username).exists():
                errors.append(ErrorDetailSchema(field="username", message="Username already exists"))

            if User.objects.filter(email=user_in.email).exists():
                errors.append(ErrorDetailSchema(field="email", message="Email already exists"))

            if errors:
                return 409, {"errors": errors}

            user = User.objects.create(
                username=user_in.username,
                password=make_password(user_in.password),
                role=user_in.role,
                email=user_in.email,
                first_name=user_in.first_name,
                last_name=user_in.last_name
            )
            user.save()
            tokens = get_tokens_for_user(user)
            return 200, TokenSchema(
                access=tokens['access'],
                refresh=tokens['refresh'],
                user_id=user.id,
                username=user.username,
                role=user.role,
            )
    except Exception as e:
        return 500, {"errors": [ErrorDetailSchema(field="non_field_errors", message=str(e))]}


@user_router.post('/login', response={200: TokenSchema, 401: ErrorResponseSchema, 500: ErrorResponseSchema})
def login(request, user_in: LoginSchema):
    try:
        user = authenticate(username=user_in.username, password=user_in.password)
        if not user:
            return 401, {"errors": [ErrorDetailSchema(field="non_field_errors", message="Invalid credentials")]}

        tokens = get_tokens_for_user(user)
        return 200, TokenSchema(
            access=tokens['access'],
            refresh=tokens['refresh'],
            user_id=user.id,
            username=user.username,
            role=user.role,
        )
    except Exception as e:
        return 500, {"errors": [ErrorDetailSchema(field="non_field_errors", message=str(e))]}


@user_router.post('/refresh', response={200: TokenRefreshSchema, 401: ErrorResponseSchema})
def refresh(request, refresh_token: RefreshTokenSchema):
    try:
        print("refresh_token:", refresh_token)
        refresh = RefreshToken(refresh_token.refresh)
        user_id = refresh['user_id']
        user = User.objects.get(id=user_id)

        tokens = get_tokens_for_user(user)

        return 200, TokenRefreshSchema(
            access=tokens['access'],
        )
    except InvalidToken as e:
        return 401, {"errors": [ErrorDetailSchema(field="non_field_errors", message=str(e))]}
    except Exception as e:
        return 401, {"errors": [ErrorDetailSchema(field="non_field_errors", message=str(e))]}


@user_router.get('/{user_id}', auth=jwt_auth,
                 response={200: ProfileSchema, 401: ErrorResponseSchema, 404: ErrorResponseSchema})
def profile(request, user_id: int):
    try:
        user = User.objects.get(id=user_id)
        profile_picture_data = None
        if user.profile_picture:
            profile_picture_data = {
                'data': base64.b64encode(user.profile_picture).decode('utf-8'),
                'type': user.profile_picture_type
            }

        return 200, ProfileSchema(
            username=user.username,
            role=user.role,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            profile_picture=profile_picture_data
        )
    except ObjectDoesNotExist:
        return 404, {"errors": [ErrorDetailSchema(field="user_id", message="User not found")]}
    except Exception as e:
        return 401, {"errors": [ErrorDetailSchema(field="non_field_errors", message=str(e))]}


@user_router.put('/{user_id}/profile', auth=jwt_auth,
                 response={200: ProfileSchema, 400: ErrorResponseSchema, 404: ErrorResponseSchema,
                           500: ErrorResponseSchema})
def update_profile(request, user_id: int, profile_data: UpdateProfileSchema):
    try:
        print(f"Received profile update request for user {user_id}: {profile_data}")
        user = User.objects.get(id=user_id)
        if user.id != request.user.id:
            return 400, {"errors": [ErrorDetailSchema(field="user_id", message="You can only update your own profile")]}

        if profile_data.first_name:
            user.first_name = profile_data.first_name
        if profile_data.last_name:
            user.last_name = profile_data.last_name

        if profile_data.profile_picture:
            profile_picture_data = base64.b64decode(profile_data.profile_picture)

            user.profile_picture = profile_picture_data

            user.profile_picture_type = 'image/jpeg'

        user.save()

        profile_picture_response = None
        if user.profile_picture:
            profile_picture_response = {
                'data': base64.b64encode(user.profile_picture).decode('utf-8'),
                'type': user.profile_picture_type
            }

        response_data = ProfileSchema(
            username=user.username,
            role=user.role,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            profile_picture=profile_picture_response
        )
        print(f"Profile update response: {response_data}")
        return 200, response_data
    except ObjectDoesNotExist:
        return 404, {"errors": [ErrorDetailSchema(field="user_id", message="User not found")]}
    except Exception as e:
        print(f"Error updating profile: {str(e)}")
        return 500, {"errors": [ErrorDetailSchema(field="non_field_errors", message=str(e))]}


@user_router.get('/{user_id}/role', auth=jwt_auth,
                 response={200: RoleResponseSchema, 404: ErrorResponseSchema, 401: ErrorResponseSchema})
def get_user_role(request, user_id: int):
    try:
        user = User.objects.get(id=user_id)
        return 200, RoleResponseSchema(role=user.role)
    except User.DoesNotExist:
        return 404, {"errors": [ErrorDetailSchema(field="user_id", message="User not found")]}
    except Exception as e:
        return 401, {"errors": [ErrorDetailSchema(field="non_field_errors", message=str(e))]}


@user_router.get('/{user_id}/classes', auth=jwt_auth, response={200: List[ClassResponseSchema], 400: dict})
def list_classes(request, user_id: int):
    user = request.user
    if user_id != user.id:
        return 400, {"error": "You can only view your own classes"}
    if user.role == 'teacher':
        classes = Class.objects.filter(teacher=user)
    else:
        classes = Class.objects.filter(memberships__student=user)
    return [ClassResponseSchema(id=class_instance.id, name=class_instance.name, teacher_id=class_instance.teacher_id,
                                tag=class_instance.tag)
            for class_instance in classes]


@user_router.get('/{user_id}/problems', auth=jwt_auth, response={200: List[ProblemSchema], 400: dict, 403: dict})
def list_teacher_problems(request, user_id: int):
    user = request.user
    if user_id != user.id:
        return 400, {"error": "You can only view your own problems"}

    if user.role != 'teacher':
        return 403, {"error": "Only teachers can access this endpoint"}

    problems = Problem.objects.filter(created_by=user)
    return 200, [ProblemSchema.from_orm(problem) for problem in problems]


@user_router.get('/{user_id}/solutions', auth=jwt_auth, response={200: List[SolutionSchema], 400: dict})
def list_user_solutions(request, user_id: int):
    user = request.user
    # if user_id != user.id:
    #     return 400, {"error": "You can only view your own solutions"}

    solutions = Solution.objects.filter(user=user)
    return [SolutionSchema.from_orm(solution) for solution in solutions]


@user_router.get('/count/{role}', auth=jwt_auth, response={200: int, 400: ErrorResponseSchema})
def get_user_count(request, role: Literal['all', 'student', 'teacher']):
    if role == 'all':
        count = User.objects.count()
        return 200, count
    if role not in ['student', 'teacher']:
        return 400, {"errors": [ErrorDetailSchema(field="role", message="Invalid role specified")]}
    count = User.objects.filter(role=role).count()
    return 200, count


@user_router.get('/', auth=jwt_auth, response={200: List[int], 500: ErrorResponseSchema})
def get_all_users_ids(request):
    try:
        user_ids = User.objects.values_list('id', flat=True)
        return 200, list(user_ids)
    except Exception as e:
        return 500, {"errors": [ErrorDetailSchema(field="non_field_errors", message=str(e))]}
