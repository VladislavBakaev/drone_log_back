# Generated by Django 3.2.8 on 2022-01-23 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drone_missions_logs', '0005_mavlinkmissionpoint'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MavLinkMissionPoint',
            new_name='MavLinkPX4MissionPoint',
        ),
    ]