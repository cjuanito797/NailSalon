# Generated by Django 4.1 on 2022-11-29 20:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Appointments", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sale",
            name="start_time",
            field=models.TimeField(
                blank=True, default=datetime.time(14, 2, 42, 593121), null=True
            ),
        ),
    ]
