# Generated by Django 4.0.2 on 2023-09-28 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_habit_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
    ]
