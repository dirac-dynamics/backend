from __future__ import unicode_literals

from django.contrib.postgres.operations import CreateExtension
from django.db import migrations
from django.utils import timezone
from django.contrib.auth import get_user_model

import os

def create_superuser(apps, schema_editor):
    superuser = get_user_model()(
        is_active=True,
        is_superuser=True,
        is_staff=True,
        username=os.environ['ADMIN_USERNAME'],
        email=os.environ['ADMIN_EMAIL'],
        last_login=timezone.now(),
    )
    superuser.set_password(os.environ['ADMIN_PASSWORD'])
    superuser.save()


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial')
    ]

    operations = [
        CreateExtension('postgis'),
        migrations.RunPython(create_superuser)
    ]