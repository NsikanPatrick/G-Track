# Generated by Django 3.2.18 on 2023-10-21 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtrack_app', '0029_auto_20231021_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='client_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='debtor_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
