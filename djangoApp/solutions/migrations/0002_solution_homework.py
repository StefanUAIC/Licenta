# Generated by Django 5.0.6 on 2024-06-15 01:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeworks', '0001_initial'),
        ('solutions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='homework',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solutions', to='homeworks.homework'),
        ),
    ]
