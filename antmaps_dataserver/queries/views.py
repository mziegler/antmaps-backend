"""
This module has all of the Django views that hit the database and process data
for Ant Maps.
"""

import json

from django.http import HttpResponse

from queries.models import Subfamily, Genus, Species, Record, Bentity



class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = json.dumps(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)




def subfamily_list(request):
    """
    Return a JSON response with a sorted list of subfamilies.  For each subfamily,
    include a {key:xxx, display:xxx} with the names to use as a database key, and
    to display to the user (the same for now.)
    """
    
    subfamilies = ( Subfamily.objects.all()
                    .order_by('subfamily_name')
                    .values_list('subfamily_name', flat=True) )
    
    json_objects = [{'key': s, 'display':s} for s in subfamilies]
    
    return JSONResponse({'subfamilies': json_objects})
    
    
    
    
def genus_list(request):
    """
    Return a JSON response with a sorted list of genera.  For each genus,
    include a {key:xxx, display:xxx} with the names to use as a database key, and
    to display to the user (the same for now.)
    
    If there's a "subfamily" provided in the query string, return only genera
    with a subfamily_name matching the supplied genus.
    """


    genera = ( Genus.objects.all()
                .order_by('genus_name')
                .values_list('genus_name', flat=True) )
                
    # if the user supplied a subfamily, get genuses with that subfamily
    if request.GET.get('subfamily'):
        genera = genera.filter(subfamily_name=request.GET.get('subfamily'))
    
    # serialize to JSON
    json_objects = [{'key': g, 'display':g} for g in genera]
    
    return JSONResponse({'genera': json_objects})
    
    
    
    
def species_list(request):
    """
    Return a JSON response with a sorted list of species.  For each species,
    include a {key:xxx, display:xxx} with the names to use as a database key, and
    to display to the user (the same for now.)
    
    If there's a "genus", "subfamily", "bentity", or "bentity2" in the query 
    string, return only species matching these supplied parameters.  
    
    Bentity and bentity2 functionally both do the same thing, and are useful
    for finding species that are present in both bentities.  If you just need one,
    use "bentity" instead of "bentity2" for slightly better performance.
    
    For now, return an empty list if there's no genus supplied.  (Will probably
    want to change this behavior later.)
    """
    
    
    filtered = False
    species = Species.objects.all().order_by('taxon_code').distinct()
    
    if request.GET.get('genus'):
        filtered = True
        species = species.filter(genus_name=request.GET.get('genus'))
        
    if request.GET.get('subfamily'):
        filtered = True
        species = species.filter(genus_name__subfamily_name=request.GET.get('subfamily'))
        
    if request.GET.get('bentity'):
        filtered = True
        species = species.filter(speciesbentitypair__bentity=request.GET.get('bentity'))
    
    # supply 'bentity2' to get species overlapping between 2 bentities    
    if request.GET.get('bentity2'): 
        filtered = True
        species_in_bentity2 = species.filter(speciesbentitypair__bentity=request.GET.get('bentity2')).distinct()
        species = species.filter(pk__in=species_in_bentity2) # intersection
        
                     
    
    # return species list if it was filtered by something    
    if filtered:
    
        # serialize to JSON            
        # s.genus_name_id gets the actual text of the genus_name, instead of the related object
        json_objects = [{
            'key': s.taxon_code, 
            'display': (s.genus_name_id + ' ' + s.species_name) 
          } for s in species]
        
        return JSONResponse({'species': json_objects})
    
    
    # error message if the user didn't supply an argument to filter the species list
    else: 
        return JSONResponse({'species': [], 'message': "Please supply a 'genus', 'subfamily', 'bentity', and/or 'bentity2' in the URL query string."})
            
       
       

def bentity_list(request):
    """
    Return a JSON response with a list of bentities for the diversity mode.
    
    For each subfamily, include a {key:xxx, display:xxx} with the names to 
    use as a database key, and to display to the user.
    """
       
       
    bentities = Bentity.objects.all().order_by('bentity')
    
    json_objects = [{
       'key': b.gid,
       'display': b.bentity,
    } for b in bentities]
    
    return JSONResponse({'bentities' : json_objects})
    
    
    
    
def species_points(request):
    """
    Return a JSON response with a list of geo points for a species.  For each record,
    include a {gabi_acc_number:xxx, lat:xxx, lon:xxx} object.
    
    A "taxon_code" must be provided in the URL query string, to specify the species.
    """
    
    if request.GET.get('taxon_code'):
        records = ( Record.objects
            .filter(taxon_code=request.GET.get('taxon_code'))
            .filter(lon__isnull=False) )
        
        # serialize to JSON
        json_objects = [{
            'gabi_acc_number': r.gabi_acc_number,
            'lat': r.lat,
            'lon': r.lon,
        } for r in records]
        
        return JSONResponse({'records': json_objects})
    
    else: # punt if the request doesn't have a taxon_code
        return JSONResponse({'records': [], 'message': "Please supply a 'taxon_code' in the URL query string."})
        
        
        

def species_per_bentity(request):
    """
    Return a JSON response with a list of bentities, and the number of categorized
    species in each bentity.  
    
    You must supply either a 'genus_name' or 'subfamily_name' in the URL query 
    string to filter species.  (If you supply both, only 'genus_name' will be used.
    
    Outputted JSON is a list with {gid:xxx, species_count:xxx} for each bentity.
    """
    
    bentities = []
    
    if request.GET.get('genus_name'): # use genus name
        bentities = Bentity.objects.raw("""
            SELECT "bentity2_id" AS "bentity2_id", count(distinct "valid_species_name") AS "species_count"
            FROM "map_species_bentity_pair"
            WHERE "genus_name" = %s
            GROUP BY "bentity2_id"     
            """, [request.GET.get('genus_name')]) 
        
    elif request.GET.get('subfamily_name'): # use subfamily name
        bentities = Bentity.objects.raw("""
            SELECT "bentity2_id" AS "bentity2_id", count(distinct "valid_species_name") AS "species_count"
            FROM "map_species_bentity_pair"
            WHERE "subfamily_name" = %s
            GROUP BY "bentity2_id"  
            """, [request.GET.get('subfamily_name')]) 
    
    else:
        return JSONResponse({'records': [], 'message': "Please supply a 'genus_name' or 'subfamily_name' in the URL query string."})
      
    # serialize to JSON    
    json_objects = [{'gid': b.gid, 'species_count': b.species_count} for b in bentities]
    
    return JSONResponse({'bentities': json_objects})
    
    
    
    
def species_in_common(request):
    """
    Given a 'bentity' in the URL query string, return a JSON response with a list
    of bentities, and a count of how many species each other bentity has in common
    with the given bentity.
    
    For each bentity, include {gid:xxx, species_count:xxx}
    """
    
    if request.GET.get('bentity'):
        bentities = Bentity.objects.raw("""
            SELECT r2."bentity2_id" AS "bentity2_id", count(distinct r2."valid_species_name") AS "species_count"
            FROM "map_species_bentity_pair" AS r1
            INNER JOIN "map_species_bentity_pair" AS r2
            ON r1."valid_species_name" = r2."valid_species_name"
            WHERE r1."bentity2_id" = %s
            GROUP BY r2."bentity2_id";
            """, [request.GET.get('bentity')])
            
        # serialize to JSON
        json_objects = [{'gid': b.gid, 'species_count': b.species_count} for b in bentities]
        
        return JSONResponse({'bentities': json_objects})
        
    else:
        return JSONResponse({'bentities':[], 'message': "Please supply a 'bentity' in the URL query string."})
        
