from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.db import transaction
from ninja import Router
from .schemas import UserSchema, TokenSchema
from rest_framework.authtoken.models import Token

User = get_user_model()

user_router = Router()


@user_router.post('/register', response=TokenSchema)
def register(request, user_in: UserSchema):
    try:
        with transaction.atomic():
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
        return {"error": str(e)}, 500


@user_router.post('/login', response=TokenSchema)
def login(request, user_in: UserSchema):
    user = authenticate(username=user_in.username, password=user_in.password)
    if not user:
        return {"error": "Invalid credentials"}
    token, _ = Token.objects.get_or_create(user=user)
    return {
        "token": token.key,
        "user_id": user.id,
        "username": user.username,
        "role": user.role,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }
