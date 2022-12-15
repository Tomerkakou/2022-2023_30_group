# Generated by Django 4.0 on 2022-12-15 12:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='descprition',
            new_name='description',
        ),
        migrations.AlterField(
            model_name='newinventory',
            name='dt',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 15, 14, 16, 54, 671658)),
        ),
        migrations.AlterField(
            model_name='orders',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 15, 14, 16, 54, 671658)),
        ),
        migrations.AlterField(
            model_name='orders',
            name='return_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 4, 14, 16, 54, 671658)),
        ),
    ]