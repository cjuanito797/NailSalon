# Generated by Django 4.1 on 2022-09-21 02:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Account", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="technician", name="pay_rate",),
    ]