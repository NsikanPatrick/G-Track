# Generated by Django 4.1 on 2023-02-21 13:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtrack_app', '0021_alter_userprofile_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 21, 13, 29, 24, 554548, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_seen',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 21, 13, 29, 24, 554548, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]