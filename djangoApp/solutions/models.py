from django.contrib.auth import get_user_model
from django.db import models

from problems.models import Problem

User = get_user_model()


class Solution(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='solutions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solutions')
    code = models.TextField()
    language_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    percentage_passed = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.problem.title}"
