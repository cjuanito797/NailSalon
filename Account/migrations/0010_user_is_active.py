# Generated by Django 4.1 on 2022-11-04 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Account", "0009_user_age"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
