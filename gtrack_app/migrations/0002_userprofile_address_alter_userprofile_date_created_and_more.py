# Generated by Django 4.1 on 2022-12-23 14:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtrack_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, max_length=65, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 23, 14, 51, 57, 415457, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_seen',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 23, 14, 51, 57, 415457, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
