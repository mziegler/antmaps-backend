"""
Right now, this module just has logic to populate the taxonomy select boxes.
"""

import json

from django.http import HttpResponse

from speciesmode.models import Subfamily, Genus, Species, Record



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
                    
        json_objects = [{
            'key': s.taxon_code, 
            'display': (s.genus_name_text + ' ' + s.species_name + ' ' + (s.subspecies_name or ''))
          } for s in species]
        
        return JSONResponse({'species': json_objects})
    
    else:
        return JSONResponse({'species': [], 'message': "Please supply a 'genus' in the URL query string."})
            
        
    
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
        
        json_objects = [{
            'gabi_acc_number': r.gabi_acc_number,
            'lat': r.lat,
            'lon': r.lon,
        } for r in records]
        
        return JSONResponse({'records': json_objects})
    
    else: # punt if the request doesn't have a taxon_code
        return JSONResponse({'records': [], 'message': "Please supply a 'taxon_code' in the URL query string."})
