# Generated by Django 5.0.6 on 2024-06-05 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('code_submission', '0004_remove_solution_updated_at_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Solution',
        ),
    ]
