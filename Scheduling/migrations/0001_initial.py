# Generated by Django 4.1 on 2022-08-31 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="timeSlots",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tech", models.EmailField(max_length=254, verbose_name="email")),
                ("dayOfWeek", models.CharField(max_length=9)),
                ("_9_00_am", models.BooleanField(default=False)),
                ("_9_15am", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="TechnicianSchedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tech",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="email"
                    ),
                ),
                ("monday_availability", models.BooleanField(default=False)),
                ("monday_timeIn", models.TimeField()),
                ("monday_timeOut", models.TimeField()),
                ("wednesday_availability", models.BooleanField(default=False)),
                ("wednesday_time_In", models.TimeField()),
                ("wednesday_time_Out", models.TimeField()),
                ("thursday_availability", models.BooleanField(default=False)),
                ("thursday_time_In", models.TimeField()),
                ("thursday_time_Out", models.TimeField()),
                ("friday_availability", models.BooleanField(default=False)),
                ("friday_time_In", models.TimeField()),
                ("friday_time_Out", models.TimeField()),
                ("saturday_availability", models.BooleanField(default=False)),
                ("saturday_time_In", models.TimeField()),
                ("saturday_time_Out", models.TimeField()),
                ("sunday_availability", models.BooleanField(default=False)),
                ("sunday_time_In", models.TimeField()),
                ("sunday_time_Out", models.TimeField()),
                ("tuesday_availability", models.BooleanField(default=False)),
                ("tuesday_time_In", models.TimeField()),
                ("tuesday_time_Out", models.TimeField()),
                (
                    "friday_timeSlots",
                    models.ForeignKey(
                        default=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fridayTimeSlots",
                        to="Scheduling.timeslots",
                    ),
                ),
                (
                    "monday_timeSlots",
                    models.ForeignKey(
                        default=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mondayTimeSlots",
                        to="Scheduling.timeslots",
                    ),
                ),
                (
                    "saturday_timeSlots",
                    models.ForeignKey(
                        default=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="saturdayTimeSlots",
                        to="Scheduling.timeslots",
                    ),
                ),
                (
                    "sunday_timeSlots",
                    models.ForeignKey(
                        default=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sundayTimeSlots",
                        to="Scheduling.timeslots",
                    ),
                ),
                (
                    "thursday_timeSlots",
                    models.ForeignKey(
                        default=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="thursdayTimeSlots",
                        to="Scheduling.timeslots",
                    ),
                ),
                (
                    "tuesday_timeSlots",
                    models.ForeignKey(
                        default=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tuesdayTimeSlots",
                        to="Scheduling.timeslots",
                    ),
                ),
                (
                    "wednesday_timeSlots",
                    models.ForeignKey(
                        default=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wednesdayTimeSlots",
                        to="Scheduling.timeslots",
                    ),
                ),
            ],
        ),
    ]