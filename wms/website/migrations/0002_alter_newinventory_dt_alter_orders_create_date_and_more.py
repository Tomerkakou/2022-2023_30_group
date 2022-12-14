# Generated by Django 4.0 on 2022-12-23 22:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newinventory',
            name='dt',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 24, 0, 29, 59, 610001)),
        ),
        migrations.AlterField(
            model_name='orders',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 24, 0, 29, 59, 610001)),
        ),
        migrations.AlterField(
            model_name='orders',
            name='return_date',
            field=models.DateTimeField(default=None),
        ),
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.IntegerField(choices=[(0, 'Waiting'), (1, 'In progress'), (2, 'Completed')], default=0),
        ),
    ]
