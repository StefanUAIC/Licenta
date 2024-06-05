from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.db import transaction
from ninja import Router
from rest_framework_simplejwt.tokens import RefreshToken

from .schemas import UserSchema, TokenSchema, ErrorResponseSchema, ErrorDetailSchema, LoginSchema

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


@user_router.get('/{user_id}', response={200: UserSchema, 401: ErrorResponseSchema})
def profile(request, user_id: int):
    try:
        user = User.objects.get(id=user_id)
        return 200, UserSchema(
            username=user.username,
            role=user.role,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name
        )
    except Exception as e:
        return 401, {"errors": [ErrorDetailSchema(field="non_field_errors", message=str(e))]}
