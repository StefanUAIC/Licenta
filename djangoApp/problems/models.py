from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Problem(models.Model):
    DIFFICULTIES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )
    CATEGORIES = (
        ('arrays', 'Arrays'),
        ('linked_lists', 'Linked Lists'),
        ('sorting', 'Sorting'),
        ('searching', 'Searching'),
        ('trees', 'Trees'),
        ('graphs', 'Graphs'),
        ('dynamic_programming', 'Dynamic Programming'),
        ('recursion', 'Recursion'),
        ('backtracking', 'Backtracking'),
        ('bit_manipulation', 'Bit Manipulation'),
        ('greedy', 'Greedy'),
        ('math', 'Math'),
        ('geometry', 'Geometry'),
        ('combinatorics', 'Combinatorics'),
        ('probability', 'Probability'),
        ('game_theory', 'Game Theory'),
        ('puzzles', 'Puzzles'),
        ('miscellaneous', 'Miscellaneous'),
    )
    GRADES = (
        (9, '9th'),
        (10, '10th'),
        (11, '11th'),
        (12, '12th'),
    )
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(choices=DIFFICULTIES, max_length=10, default='easy')
    example_input = models.TextField()
    example_output = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problems')
    solution_code = models.TextField()
    grade = models.IntegerField(choices=GRADES, default=9)
    category = models.CharField(choices=CATEGORIES, max_length=20, default='miscellaneous')
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='PENDING')

    def __str__(self):
        return self.title


class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    stdin = models.TextField()
    expected_output = models.TextField()

    def __str__(self):
        return f"TestCase for {self.problem.title}"
