# Generated by Django 4.0.2 on 2023-10-03 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_day_color_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='date',
            field=models.DateField(),
        ),
    ]
