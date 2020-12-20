from django.db import models
from django.contrib.gis.db.models import PointField

class Carrier(models.Model):
    position = PointField()
    phone = models.CharField(max_length=20)
    driver = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=10)

class Transportable(models.Model):
    position = PointField()
    sender = models.CharField(max_length=200)
    receiver = models.CharField(max_length=200)