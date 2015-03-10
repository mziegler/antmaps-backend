from django.shortcuts import render
from django.contrib.gis.geos import Polygon # for bounding box

from bentities.models import Bentity

# Create your views here.

def bentities_in_boundingbox(xmin, ymin, xmax, ymax):
    """
    Given a bounding box in longitude,latitude as xmin, ymin, xmax, ymax;
    return a queryset of bentities that overlap with the bounding box.
    
    (Useful for getting all of the bentities/polygons for the part of the map
    that the user is currently zoomed in to)
    """

    bbox = (xmin, ymin, xmax, ymax)
    geom = Polygon.from_bbox(bbox)
  
    return Bentity.objects.filter(geog__bboverlaps=geom)
  

