"""
Right now, this module just has logic to populate the taxonomy select boxes.
"""

import json

from django.http import HttpResponse

from speciesmode.models import Subfamily, Genus, Species



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
            'display': (s.genus_name_text + ' ' + s.species_name + ' ' + s.subspecies_name)
          } for s in species]
        
    else:
        json_objects = []
        
    return JSONResponse({'species': json_objects})
