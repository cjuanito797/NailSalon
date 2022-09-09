# Generated by Django 4.1 on 2022-09-07 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Appointments", "0004_alter_service_duration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service", name="duration", field=models.DurationField(),
        ),
        migrations.CreateModel(
            name="Appointment",
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
                    "services",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="services",
                        to="Appointments.service",
                    ),
                ),
            ],
        ),
]