# Generated by Django 3.1.7 on 2021-03-31 18:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0002_auto_20210320_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_Type',
            field=models.CharField(choices=[('F', 'Movie'), ('T', 'TV'), ('M', 'Music')], default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='owned_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
