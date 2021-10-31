# Generated by Django 3.2.8 on 2021-10-29 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='YDLogFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(upload_to='logs/')),
            ],
            options={
                'db_table': 'yd_drone_logs_file',
            },
        ),
    ]