# Generated by Django 5.0.6 on 2024-06-05 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_submission', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solution',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='solution',
            name='percentage_passed',
            field=models.IntegerField(default=0),
        ),
    ]
