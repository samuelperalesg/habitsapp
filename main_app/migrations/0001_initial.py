# Generated by Django 4.0.2 on 2022-02-22 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('habit_name', models.CharField(max_length=100)),
                ('healthy', models.BooleanField()),
                ('plan_of_action', models.TextField(max_length=250)),
                ('external_cue', models.CharField(max_length=100)),
                ('internal_cue', models.CharField(max_length=100)),
            ],
        ),
    ]