# Generated by Django 4.1 on 2022-11-20 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0010_user_is_active'),
        ('Appointments', '0003_appointment_services_alter_sale_technician'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], default='active', max_length=10),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='technician',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Account.technician'),
        ),
    ]