from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.db import transaction
from ninja import Router
from rest_framework.authtoken.models import Token

from .schemas import UserSchema, TokenSchema, ErrorResponseSchema, LoginSchema

User = get_user_model()

user_router = Router(tags=["Users"])


@user_router.post('/register', response={200: TokenSchema, 409: ErrorResponseSchema, 500: ErrorResponseSchema})
def register(request, user_in: UserSchema):
    try:
        with transaction.atomic():
            if User.objects.filter(username=user_in.username).exists():
                return 409, {"error": "Username already exists"}

            if User.objects.filter(email=user_in.email).exists():
                return 409, {"error": "Email already exists"}

            user = User.objects.create(
                username=user_in.username,
                password=make_password(user_in.password),
                role=user_in.role,
                email=user_in.email,
                first_name=user_in.first_name,
                last_name=user_in.last_name
            )
            token, _ = Token.objects.get_or_create(user=user)
            return TokenSchema(
                token=token.key,
                user_id=user.id,
                username=user.username,
                role=user.role,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name
            )
    except Exception as e:
        return 500, {"error": str(e)}


@user_router.post('/login', response={200: TokenSchema, 401: ErrorResponseSchema, 500: ErrorResponseSchema})
def login(request, user_in: LoginSchema):
    try:
        user = authenticate(username=user_in.username, password=user_in.password)
        if not user:
            return 401, {"error": "Invalid credentials"}

        token, _ = Token.objects.get_or_create(user=user)
        return TokenSchema(
            token=token.key,
            user_id=user.id,
            username=user.username,
            role=user.role,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name
        )
    except Exception as e:
        return 500, {"error": str(e)}


@user_router.get('/logout', response={200: dict, 401: ErrorResponseSchema})
def logout(request):
    try:
        request.user.auth_token.delete()
        return 200, {}
    except Exception as e:
        return 401, {"error": str(e)}


@user_router.get('/profile', response={200: UserSchema, 401: ErrorResponseSchema})
def profile(request):
    try:
        user = request.user
        return UserSchema(
            username=user.username,
            role=user.role,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name
        )
    except Exception as e:
        return 401, {"error": str(e)}
