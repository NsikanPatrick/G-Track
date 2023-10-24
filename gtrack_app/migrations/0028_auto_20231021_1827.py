# Generated by Django 3.2.18 on 2023-10-21 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gtrack_app', '0027_auto_20231021_1410'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='client_id',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='debtor_id',
        ),
        migrations.AddField(
            model_name='payment',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment',
            name='debtor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gtrack_app.debtor'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='time_sent',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
