import re
from base64 import b64encode
from enum import Enum
from typing import Literal, Optional

from ninja import Schema
from pydantic import BaseModel
from pydantic import EmailStr, constr, field_validator


class RoleEnum(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"


class UserSchema(Schema):
    username: constr(min_length=5, max_length=30, pattern=r'^[a-zA-Z0-9_]*$')
    password: constr(min_length=8, max_length=30, pattern=r'^[a-zA-Z0-9_@$!%*?&]*$')
    role: RoleEnum
    email: EmailStr
    first_name: constr(min_length=1, max_length=30, pattern=r'^[a-zA-Z]*$')
    last_name: constr(min_length=1, max_length=30, pattern=r'^[a-zA-Z]*$')

    @field_validator('password')
    def password_complexity(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[@$!%*?&]', v):
            raise ValueError('Password must contain at least one special character')
        return v


class LoginSchema(Schema):
    username: str
    password: str


class TokenSchema(Schema):
    access: str
    refresh: str
    user_id: int
    username: str
    role: str


class ErrorDetailSchema(Schema):
    field: str
    message: str


class ErrorResponseSchema(Schema):
    errors: list[ErrorDetailSchema]


class ProfilePictureSchema(BaseModel):
    type: str
    data: str


class ProfileSchema(Schema):
    username: str
    role: str
    email: str
    first_name: str
    last_name: str
    profile_picture: Optional[ProfilePictureSchema] = None

    @classmethod
    def from_orm(cls, obj):
        data = {
            "username": obj.username,
            "role": obj.role,
            "email": obj.email,
            "first_name": obj.first_name,
            "last_name": obj.last_name,
        }

        if obj.profile_picture and obj.profile_picture_type:
            data["profile_picture"] = ProfilePictureSchema(
                type=obj.profile_picture_type,
                data=b64encode(obj.profile_picture).decode('utf-8')
            )

        return cls(**data)


class TokenRefreshSchema(Schema):
    access: str


class RefreshTokenSchema(Schema):
    refresh: str


class RoleResponseSchema(Schema):
    role: str


class UpdateProfileSchema(Schema):
    first_name: constr(min_length=1, max_length=30, pattern=r'^[a-zA-Z]*$')
    last_name: constr(min_length=1, max_length=30, pattern=r'^[a-zA-Z]*$')
    profile_picture: str | None
