# Generated by Django 4.1 on 2023-01-23 20:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtrack_app', '0009_debtor_due_date_alter_userprofile_date_created_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debtor_id', models.IntegerField(blank=True, null=True)),
                ('client_id', models.IntegerField(blank=True, null=True)),
                ('medium_of_payment', models.CharField(blank=True, max_length=65, null=True)),
                ('amount_payed', models.CharField(blank=True, max_length=65, null=True)),
                ('amount_owed', models.CharField(blank=True, max_length=65, null=True)),
                ('balance_left', models.CharField(blank=True, max_length=65, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 23, 20, 59, 8, 265973, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_seen',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 1, 23, 20, 59, 8, 265973, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
