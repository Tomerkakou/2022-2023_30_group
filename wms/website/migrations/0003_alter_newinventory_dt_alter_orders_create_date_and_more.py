# Generated by Django 4.0 on 2022-12-23 22:32

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_alter_newinventory_dt_alter_orders_create_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newinventory',
            name='dt',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 24, 0, 32, 24, 303080)),
        ),
        migrations.AlterField(
            model_name='orders',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 24, 0, 32, 24, 303080)),
        ),
        migrations.AlterField(
            model_name='orders',
            name='return_date',
            field=models.DateTimeField(default=django.db.models.deletion.SET_NULL, null=True),
        ),
    ]