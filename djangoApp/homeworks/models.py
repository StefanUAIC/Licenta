from django.db import models
from problems.models import Problem
from classes.models import Class


class Homework(models.Model):
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='homeworks')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='homeworks')
    due_date = models.DateTimeField()
