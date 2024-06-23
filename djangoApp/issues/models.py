from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

User = get_user_model()


class Issue(models.Model):
    title = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(3, "Title must be at least 3 characters long.")]
    )
    description = models.TextField(
        validators=[MinLengthValidator(5, "Description must be at least 5 characters long.")]
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
