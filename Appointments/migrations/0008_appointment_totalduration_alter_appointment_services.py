# Generated by Django 4.1 on 2022-09-07 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Appointments", "0007_remove_appointment_services_appointment_services"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="totalDuration",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="appointment",
            name="services",
            field=models.ManyToManyField(
                default=None, related_name="services", to="Appointments.service"
            ),
        ),
<<<<<<< HEAD
    ]
=======
    ]
>>>>>>> 528aa387078ca6a132ffa581ee78b5c1a0a13164
