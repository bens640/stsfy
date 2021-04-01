# Generated by Django 3.1.7 on 2021-03-31 19:09

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210331_1351'),
        ('library', '0006_auto_20210331_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useritem',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 31, 15, 9, 7, 326769)),
        ),
        migrations.AlterField(
            model_name='useritem',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.group'),
        ),
    ]
