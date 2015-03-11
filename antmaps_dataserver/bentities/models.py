# import GeoDjango models
from django.contrib.gis.db import models

# Create your models here.

class Bentity(models.Model):
  gid = models.IntegerField(primary_key=True)
  bentity = models.CharField(max_length=41, blank=True)
  geog = models.GeometryField(blank=True, srid=4326)
  
  class Meta:
    managed = False
    db_table = 'bentities_highres'

