# Generated by Django 3.1.7 on 2021-03-31 19:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_auto_20210331_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useritem',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 31, 15, 10, 42, 405956)),
        ),
    ]