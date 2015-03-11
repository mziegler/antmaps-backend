"""
A function for finding the bentities within a bounding box, and a view for
returning polygons of bentities in a bounding box.
"""


from django.http import HttpResponse
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
  

"""
We don't actually need a view to return bentities as geoJSON anymore

from djgeojson.serializers import Serializer as GeoJSONSerializer
def bentity_polygons(request):
    
    try:
        bbox = [float(bound) for bound in request.GET['bbox'].split(',')]
    except (AttributeError, ValueError):
        bbox = [-180, -90, 180, 90] # use whole globe if no bbox provided
        
    bentities = bentities_in_boundingbox(*bbox)
    
    geojson = GeoJSONSerializer().serialize(bentities, geometry_field='geog', precision=8, simplify=0.5)
    
    return HttpResponse(geojson)
"""    
