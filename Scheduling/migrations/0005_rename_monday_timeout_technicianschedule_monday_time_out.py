# Generated by Django 4.1 on 2022-10-08 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Scheduling", "0004_rename_monday_timein_technicianschedule_monday_time_in"),
    ]

    operations = [
        migrations.RenameField(
            model_name="technicianschedule",
            old_name="monday_timeOut",
            new_name="monday_time_Out",
        ),
    ]
