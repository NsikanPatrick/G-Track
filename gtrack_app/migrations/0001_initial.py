# Generated by Django 4.1.4 on 2022-12-12 22:59

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=65, null=True)),
                ('privilege', models.CharField(blank=True, max_length=50, null=True)),
                ('ip_address', models.CharField(blank=True, max_length=50, null=True)),
                ('date_created', models.DateTimeField(default=datetime.datetime(2022, 12, 12, 22, 59, 3, 446582, tzinfo=datetime.timezone.utc))),
                ('last_seen', models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 12, 22, 59, 3, 446582, tzinfo=datetime.timezone.utc), null=True)),
                ('profile_pic', models.FileField(blank=True, null=True, upload_to='uploads/profile_pictures', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
