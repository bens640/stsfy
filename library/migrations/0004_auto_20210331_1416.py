# Generated by Django 3.1.7 on 2021-03-31 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20210331_1409'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='item_Type',
            new_name='item_type',
        ),
        migrations.AddField(
            model_name='item',
            name='item_id',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
