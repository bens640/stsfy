# Generated by Django 3.1.7 on 2021-03-31 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210331_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpeg', upload_to='profile_pics'),
        ),
    ]
