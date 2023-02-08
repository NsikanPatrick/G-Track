# Generated by Django 4.1.4 on 2023-02-02 15:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtrack_app', '0013_remove_payment_due_date_payment_date_payed_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='amount_owed',
            new_name='status',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 2, 15, 19, 37, 742530, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_seen',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 2, 15, 19, 37, 742530, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
