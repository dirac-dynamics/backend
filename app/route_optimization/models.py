from django.db import models
from django.contrib.gis.db.models import PointField

# Create your models here.
class Carrier(models.Model):
    position = PointField()

class Transportable(models.Model):
    position = PointField()
    destination = PointField()