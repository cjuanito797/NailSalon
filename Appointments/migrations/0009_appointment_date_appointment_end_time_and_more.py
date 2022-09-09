# Generated by Django 4.1 on 2022-09-07 21:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("Appointments", "0008_appointment_totalduration_alter_appointment_services"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="date",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="appointment",
            name="end_time",
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="appointment",
            name="start_time",
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="appointment",
            name="totalCharge",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
            preserve_default=False,
        ),
    ]
