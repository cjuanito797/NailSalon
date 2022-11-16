# Generated by Django 4.1 on 2022-11-02 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appointments', '0008_alter_appointment_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='completed',
        ),
        migrations.AddField(
            model_name='sale',
            name='status',
            field=models.CharField(choices=[('scheduled', 'scheduled'), ('working', 'working'), ('closed', 'closed'), ('canceled', 'canceled')], default='scheduled', max_length=10),
        ),
    ]
