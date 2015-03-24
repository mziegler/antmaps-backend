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
    
    If there's a "genus" in the query string, return only species with a
    genus_name matching the supplied genus.
    
    For now, return an empty list if there's no genus supplied.  (Will probably
    want to change this behavior later.)
    """
    
    if request.GET.get('genus'):
        species = ( Species.objects.all()
                    .filter(genus_name=request.GET.get('genus'))
                    .order_by('species_name') )
        
        # serialize to JSON            
        # s.genus_name_id gets the actual text of the genus_name, instead of the related object
        json_objects = [{
            'key': s.taxon_code, 
            'display': (s.genus_name_id + ' ' + s.species_name + ' ' + (s.subspecies_name or '')) 
          } for s in species]
        
        return JSONResponse({'species': json_objects})
    
    else:
        return JSONResponse({'species': [], 'message': "Please supply a 'genus' in the URL query string."})
            
       
       

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
            SELECT "record"."bentity" as "gid", count(distinct "record"."valid_taxonomy") as "species_count"
            FROM "record" 
            INNER JOIN "species"
            ON "record"."valid_taxonomy" = "species"."taxon_code"
            where "species"."genus_name" = %s
            group by "record"."bentity"     
            """, [request.GET.get('genus_name')]) 
        
    elif request.GET.get('subfamily_name'): # use subfamily name
        bentities = Bentity.objects.raw("""
            SELECT "record"."bentity" as "gid", count(distinct "record"."valid_taxonomy") as "species_count"
            FROM "record" 
            INNER JOIN "species"
            ON "record"."valid_taxonomy" = "species"."taxon_code"
            INNER JOIN "genus"
            ON "genus"."genus_name" = "species"."genus_name"
            where "genus"."subfamily_name" = %s
            group by "record"."bentity"  
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
            SELECT r2."bentity" AS "gid", count(distinct r2."valid_taxonomy") AS "species_count"
            FROM "record" AS r1
            INNER JOIN "record" AS r2
            ON r1."valid_taxonomy" = r2."valid_taxonomy"
            WHERE r1."bentity" = %s
            GROUP BY r2."bentity";
            """, [request.GET.get('bentity')])
            
        # serialize to JSON
        json_objects = [{'gid': b.gid, 'species_count': b.species_count} for b in bentities]
        
        return JSONResponse({'bentities': json_objects})
        
    else:
        return JSONResponse({'bentities':[], 'message': "Please supply a 'bentity' in the URL query string."})
