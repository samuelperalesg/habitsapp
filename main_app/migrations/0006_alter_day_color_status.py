# Generated by Django 4.0.2 on 2023-10-04 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_day_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='color_status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
