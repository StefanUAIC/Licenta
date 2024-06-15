import uuid

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

from problems.models import Problem

User = get_user_model()


class Class(models.Model):
    tag_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9]*$',
        message='Tag-ul poate conține doar litere și cifre.'
    )
    tag = models.CharField(max_length=3, validators=[tag_validator])
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_classes')
    created_at = models.DateTimeField(auto_now_add=True)
    join_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)


class Membership(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_memberships')
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='memberships')
