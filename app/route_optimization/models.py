from django.contrib.gis.db import models
from django.contrib.postgres.operations import CreateExtension
from django.db import migrations

# Create your models here.

class Migration(migrations.Migration):

    operations = [
        CreateExtension('postgis'),
    ]