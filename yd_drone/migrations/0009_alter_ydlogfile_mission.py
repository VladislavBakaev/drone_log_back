# Generated by Django 3.2.8 on 2021-11-08 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yd_drone', '0008_ydmissionpoint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ydlogfile',
            name='mission',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='yd_drone.ydmission'),
        ),
    ]
