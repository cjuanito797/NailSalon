# Generated by Django 4.1 on 2022-09-06 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Scheduling", "0005_rename__10_00_am_timeslots_eleven_00_am_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="timeslots", old_name="twelve_15am", new_name="twelve_15pm",
        ),
        migrations.RenameField(
            model_name="timeslots", old_name="twelve_30am", new_name="twelve_30pm",
        ),
        migrations.RenameField(
            model_name="timeslots", old_name="twelve_45am", new_name="twelve_45pm",
        ),
    ]