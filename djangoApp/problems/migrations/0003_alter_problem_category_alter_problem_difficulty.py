# Generated by Django 5.0.6 on 2024-06-05 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='category',
            field=models.CharField(choices=[('arrays', 'Arrays'), ('linked_lists', 'Linked Lists'), ('sorting', 'Sorting'), ('searching', 'Searching'), ('trees', 'Trees'), ('graphs', 'Graphs'), ('dynamic_programming', 'Dynamic Programming'), ('recursion', 'Recursion'), ('backtracking', 'Backtracking'), ('bit_manipulation', 'Bit Manipulation'), ('greedy', 'Greedy'), ('math', 'Math'), ('geometry', 'Geometry'), ('combinatorics', 'Combinatorics'), ('probability', 'Probability'), ('game_theory', 'Game Theory'), ('puzzles', 'Puzzles'), ('miscellaneous', 'Miscellaneous')], default='miscellaneous'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='difficulty',
            field=models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='easy'),
        ),
    ]