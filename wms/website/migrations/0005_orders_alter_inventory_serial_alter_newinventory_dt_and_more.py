# Generated by Django 4.0 on 2022-12-07 10:32

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_inventory_available_alter_inventory_serial_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='orders',
            fields=[
                ('order_number', models.AutoField(primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(default=datetime.datetime(2022, 12, 7, 12, 32, 4, 236815))),
                ('return_date', models.DateTimeField(default=datetime.datetime(2022, 12, 27, 12, 32, 4, 236815))),
                ('status', models.IntegerField(choices=[(0, 'waiting'), (1, 'completed'), (2, 'collected')], default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='inventory',
            name='serial',
            field=models.IntegerField(blank=True, default=django.db.models.deletion.SET_NULL, unique=True),
        ),
        migrations.AlterField(
            model_name='newinventory',
            name='dt',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 7, 12, 32, 4, 236815)),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(0, 'manager'), (1, 'worker'), (2, 'student')], default=2),
        ),
        migrations.CreateModel(
            name='specific_order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0, message='amount must be greater than 0')])),
                ('completed', models.BooleanField(default=False)),
                ('inventory_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.inventory')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.orders')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='website.products')),
            ],
        ),
        migrations.AddField(
            model_name='orders',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='website.user'),
        ),
    ]