# Generated by Django 3.2.8 on 2021-10-20 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mission_name', models.CharField(max_length=150)),
                ('at_create', models.DateTimeField()),
            ],
            options={
                'db_table': 'mission_info',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_user_name', models.CharField(max_length=150)),
                ('ip_address', models.GenericIPAddressField()),
                ('operation_system', models.CharField(max_length=150)),
                ('ardupilot_version', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'user_info',
            },
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('param1', models.DecimalField(decimal_places=9, max_digits=15)),
                ('param2', models.DecimalField(decimal_places=9, max_digits=15)),
                ('param3', models.DecimalField(decimal_places=9, max_digits=15)),
                ('param4', models.DecimalField(decimal_places=9, max_digits=15)),
                ('x', models.DecimalField(decimal_places=9, max_digits=15)),
                ('y', models.DecimalField(decimal_places=9, max_digits=15)),
                ('z', models.DecimalField(decimal_places=9, max_digits=15)),
                ('seq', models.IntegerField()),
                ('command', models.IntegerField()),
                ('target_system', models.IntegerField()),
                ('target_component', models.IntegerField()),
                ('frame', models.IntegerField()),
                ('current', models.IntegerField()),
                ('autocontinue', models.IntegerField()),
                ('mission_type', models.IntegerField()),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mission.mission')),
            ],
            options={
                'db_table': 'point_info',
            },
        ),
        migrations.AddField(
            model_name='mission',
            name='user_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mission.userinfo'),
        ),
    ]
