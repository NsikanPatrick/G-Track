# Generated by Django 4.1.4 on 2023-01-30 22:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtrack_app', '0012_rename_payments_payment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='due_date',
        ),
        migrations.AddField(
            model_name='payment',
            name='date_payed',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 30, 22, 3, 15, 886871, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_seen',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 1, 30, 22, 3, 15, 886871, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
