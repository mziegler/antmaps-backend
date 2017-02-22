"""
This module has all of the Django views that hit the database and process data
for Ant Maps.
"""

import csv
import json
from re import split
from io import StringIO

from django.http import HttpResponse, StreamingHttpResponse
from django.db.models import Q
from django.views.decorators.cache import never_cache

from queries.models import Subfamily, Genus, Species, Record, Bentity, SpeciesBentityPair, Taxonomy, SpeciesPoints





class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = json.dumps(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class CSVResponse(HttpResponse):
    """
    An HttpResponse that renders its contents as a CSV.
    
    'rows' should be a list of dict objects, with each entry corresponding to 1 CSV field.
    'fields' is the ordered list of field names in the CSV.
    """
    def __init__(self, rows, fields, **kwargs):
               
        csvfile = StringIO()
        
        # Write header with field names
        headerwriter = csv.writer(csvfile)    
        headerwriter.writerow(fields)
                                      
        # Write CSV rows
        writer = csv.DictWriter(csvfile, fields, extrasaction='ignore')
        for row in rows:
            writer.writerow(row)
            
            
        kwargs['content_type'] = 'text/csv'
        super(CSVResponse, self).__init__(csvfile.getvalue(), **kwargs)
        self['Content-Disposition'] = 'attachment'




def errorResponse(errormessage, format, extraJSON={}):
    """
    A nice standardized way to show the user an error message.
    """    
    
    if format == 'csv':
        return CSVResponse(
            [{'errormessage': errormessage}],
            fields=('errormessage',)  )
            
    else:
        json_objects = extraJSON.copy()
        json_objects['error'] = True
        json_objects['errormessage'] = errormessage
        return JSONResponse(json_objects)




def subfamily_list(request, format='json'):
    """
    Return a JSON response with a sorted list of subfamilies.  For each subfamily,
    include a {key:xxx, display:xxx} with the names to use as a database key, and
    to display to the user (the same for now.)
    """
    
    subfamilies = ( Subfamily.objects.all()
                    .order_by('subfamily_name')
                    .values_list('subfamily_name', flat=True) )
                    
                        
    
    if format == 'csv':
        return CSVResponse(
            [{'subfamily':s} for s in subfamilies], 
            fields=('subfamily',)  )
        
    else:
        json_objects = [{'key': s, 'display':s} for s in subfamilies]
        return JSONResponse({'subfamilies': json_objects})
    
    
    
    
    
    
def genus_list(request, format='json'):
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
        genera = genera.filter(subfamily_name=request.GET.get('subfamily').capitalize())
    
    
    
    if format == 'csv':
        return CSVResponse(
            [{'genus': g} for g in genera], 
            fields=('genus',)   )
            
    else:
        # serialize to JSON
        json_objects = [{'key': g, 'display':g} for g in genera]
        return JSONResponse({'genera': json_objects})
    
    
    
    
    
    
    
    
def species_list(request, format='json'):
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
    
    
    filtered = False # make sure we're filtering by something
    species = Species.objects.all().order_by('taxon_code')
    
    if request.GET.get('genus'):
        filtered = True
        species = species.filter(genus_name=request.GET.get('genus').capitalize())
        
    if request.GET.get('subfamily'):
        filtered = True
        species = species.filter(genus_name__subfamily_name=request.GET.get('subfamily').capitalize())
        
    # speciesbentitypair__status='N' for only native species
    bentity = request.GET.get('bentity_id') 
    if bentity:
        filtered = True
        species = species.filter(speciesbentitypair__bentity=bentity, speciesbentitypair__category='N')
    
    # supply 'bentity2' to get species overlapping between 2 bentities
    # speciesbentitypair__status='N' for only native species    
    bentity2 = request.GET.get('bentity2_id')
    if bentity2: 
        filtered = True
        species_in_bentity2 = species.filter(speciesbentitypair__bentity=bentity2, speciesbentitypair__category='N').distinct()
        species = species.filter(pk__in=species_in_bentity2) # intersection


    	
    
    # error message if the user didn't supply an argument to filter the species list
    if not filtered: 
        return errorResponse("Please supply a 'genus', 'subfamily', 'bentity', and/or 'bentity2' argument.", format, {"species":[]})
         
    
    # return species list if it was filtered by something
    # s.genus_name_id gets the actual text of the genus_name, instead of the related object     
    else:
       
        
        if format == 'csv':
            # serialize to CSV
            return CSVResponse( 
                [{'species': s.taxon_code} for s in species], 
                fields=('species',)    )
            
        
        else:
            # serialize to JSON
            json_objects = [{'key': s.taxon_code, 'display': (s.genus_name_id + ' ' + s.species_name)} for s in species]
            return JSONResponse({'species': json_objects})







# currently doesn't do anything with the format argument
# (not a part of the public API)
def antweb_links(request, format='json'):
	"""
	Given a taxon code in the URL query string, returns a JSON response with the species,
	genus and subfamily. Outputted JSON is a list with {key:xxx, speciesName: xxx, genusName: xxx, 
	subfamilyName: xxx}
    
    Given a genus name in the URL query string, returns a JSON response with the genus and
    subfamily. Outputted JSON is a list with {key:xxx, subfamily:xxx}
		
	"""


	taxonomy = []
	if request.GET.get('taxon_code'):
		taxonomy = Taxonomy.objects.raw("""
		SELECT taxon_code, subfamily_name, genus_name, species_name
		FROM map_taxonomy_list
		WHERE taxon_code = %s
		""", [request.GET.get('taxon_code')])
		
		# serialize to JSON
		json_objects = [{'key': t.taxon_code, 'speciesName': t.species_name, 'genusName': t.genus_name, 'subfamilyName': t.subfamily_name} for t in taxonomy]
		
		return JSONResponse({'taxonomy': json_objects})
		
	elif request.GET.get('genus_name'):
		taxonomy = Taxonomy.objects.raw("""
		SELECT genus_name, subfamily_name,taxon_code
		FROM map_taxonomy_list
		WHERE genus_name = %s
		GROUP BY genus_name, subfamily_name,taxon_code
		""", [request.GET.get('genus_name')])
		
		# serialize to JSON
		json_objects = [{'key': t.genus_name, 'subfamilyName': t.subfamily_name} for t in taxonomy]
		
		return JSONResponse({'taxonomy': json_objects})
	
	else:
		return JSONResponse({'taxonomy': []})




@never_cache
def species_autocomplete(request, format='json'):
    """
    Given a query 'q' in the URL query string, split q into tokens and return
    a list of species for which the tokens in q are a prefix of the genus name
    or species name.  (Used for species-search autocomplete.)
    
    For each species, return a {label: -species name-, value: -species_code-} object.
    """
    
    if request.GET.get('q'):
        q = request.GET.get('q')
        
        species = Species.objects.all().order_by('taxon_code')
        
        # split tokens by period or white space
        q_tokens = split(r'[.\s]+', q)
        
        # prefix match for each token in the search string against genus name or species name
        for token in q_tokens:
            species = species.filter(Q(species_name__istartswith=token) | Q(genus_name__genus_name__istartswith=token))
        
    
    
    
    # empty species list if no query provided by the user
    else:
        species = []
    

        
            
    if format == 'csv':
        # serialize results as CSV
        return CSVResponse(
             [{'species': s.taxon_code} for s in species], 
             fields=('species',)  )
        
                
    else:
        # serialize results as JSON
        JSON_objects = [{'label': (s.genus_name_id + ' ' + s.species_name), 'value': s.taxon_code} for s in species]
        return JSONResponse({'species': JSON_objects})
        
        






def bentity_autocomplete(request, format='json'):
    """
    Return a list of bentities with names containing the query argument 'q'.
    Return an empty list if no argument given.
    """
        
    if request.GET.get('q'):
        q = request.GET.get('q')
        
        bentities = Bentity.objects.all().order_by('bentity')
    
        # split tokens by period or white space
        q_tokens = split(r'[.\s]+', q)
   
        # prefix match for each token in the search string against genus name or species name
        for token in q_tokens:
            bentities = bentities.filter(bentity__icontains=token)
        
    
    else:
        bentities = []
        
        
    if format == 'csv':
        # Serislize CSV for API
        return CSVResponse(
            [{'bentity_id': b.gid, 'bentity_name': b.bentity} for b in bentities],
            ('bentity_id', 'bentity_name')   )
    
    else:
        # Serialize JSON for bentity-list widget
        json_objects = [{
            'bentity_id': b.gid,
            'bentoty_name': b.bentity,
            } for b in bentities]
        return JSONResponse({'bentities' : json_objects})




       
       

def bentity_list(request, format='json'):
    """
    Return a JSON response with a list of bentities for the diversity mode.
    
    For each subfamily, include a {key:xxx, display:xxx} with the names to 
    use as a database key, and to display to the user.
    """
       
       
    bentities = Bentity.objects.all().order_by('bentity')
    
    
    if format == 'csv':
        # Serislize CSV for API
        return CSVResponse(
            [{'bentity_id': b.gid, 'bentity_name': b.bentity} for b in bentities],
            ('bentity_id', 'bentity_name')   )
    
    else:
        # Serialize JSON for bentity-list widget
        json_objects = [{
           'key': b.gid,
           'display': b.bentity,
        } for b in bentities]
    
        return JSONResponse({'bentities' : json_objects})
    
    
    
    
    
    
def species_points(request, format='json'):
    """
    Return a response with a list of geo points for a species.  For each record,
    include a {gabi_acc_number:xxx, lat:xxx, lon:xxx, status:x} object.
    
    A "species" must be provided in the URL query string, to specify the species.
    """
    
    
    species = request.GET.get('species')
    if species:
        records = ( SpeciesPoints.objects
            .filter(valid_species_name=species)
            .filter(lon__isnull=False)
            .filter(lat__isnull=False) )
        
        
        if request.GET.get('lon'):
            records = records.filter(lon=request.GET.get('lon'))
            
        if request.GET.get('lat'):
            records = records.filter(lat=request.GET.get('lat'))
            
        if request.GET.get('max_lat'):
            records = records.filter(lat__lte=request.GET.get('max_lat'))
            
        if request.GET.get('max_lon'):
            records = records.filter(lon__lte=request.GET.get('max_lon'))
        
        if request.GET.get('min_lat'):
            records = records.filter(lat__gte=request.GET.get('min_lat'))
            
        if request.GET.get('min_lon'):
            records = records.filter(lon__gte=request.GET.get('min_lon'))
        
        if request.GET.get('bentity_id'):
            records = records.filter(bentity_id=request.GET.get('bentity_id'))        
        
        
        
        # fetch all the bentitites at once, so we don't have to hit the database once for each record
        records = records.prefetch_related('bentity') 
        
        # serialize to JSON
        export_objects = [{
            'gabi_acc_number': r.gabi_acc_number,
            'species': species,
            'lat': r.lat,
            'lon': r.lon,
            'status':r.status,
            'bentity_id': r.bentity_id,
            'bentity_name': r.bentity.bentity,
            'num_records': r.num_records,
            'literature_count': r.literature_count,
            'museum_count': r.museum_count,
            'database_count': r.database_count,
        } for r in records]
        
        
        if format == 'csv':
            return CSVResponse(
                export_objects,
                fields=('species', 'lat', 'lon', 'bentity_id', 'bentity_name', 'status', 'num_records', 'literature_count', 'museum_count', 'database_count') )
        
        else:        
            return JSONResponse({'records': export_objects})
    
    else: # punt if the request doesn't have a species
        return errorResponse("Please supply a 'species' argument.", format, {'records':[]})
        
        
        
        

def species_metadata(request, format='json'):
	"""
    Return citations?
    
    Deprecating this in favor of citation_records
	"""
	
	records=[]
	if request.GET.get('taxon_code'):
		records = Record.objects.raw("""
			SELECT "gabi_acc_number", "type_of_data", "citation"
			FROM "map_record"
			WHERE "valid_species_name" = %s
			AND "bentity2_id" = %s
			""",[request.GET.get('taxon_code'),request.GET.get('bentity')])
	else: # no filter supplied
		return errorResponse("Please supply a 'taxon_code' argument.", format, {'records':[]})
		
	# serialize to JSON    
	json_objects = [{'gabi_acc_number': r.gabi_acc_number, 'type_of_data': r.type_of_data, 'citation':r.citation} for r in records]
	
	return JSONResponse({'records': json_objects})
        
        
        
        
        
def citations(request, format='json'):
    """
    Citations -- each record from this resource represents one 
    species-location-citation combination.
    
    Since we have so many records in the map_record table, there's a danger here
    of clobbering our server (and clobbering the user) with too many records at
    once.  Therefore, to keep the results sets small, there are 3 ways the user
    can query the resource:
    
    1) gabi_acc_number
    2) species AND bentity
    3) lat AND lon
    """
    
    filtered = False # make sure we're filtering by something
    records = Record.objects.all() #.order_by('gabi_acc_number')
    
    
    # accession number
    if request.GET.get('gabi_acc_number'):
        filtered = True
        records = records.filter(gabi_acc_number=request.GET.get('gabi_acc_number').upper())
    
    # species AND bentity
    if request.GET.get('species') and request.GET.get('bentity_id'):
        filtered = True
        records = records.filter(valid_species_name_id=request.GET.get('species').capitalize())
        records = records.filter(bentity_id=request.GET.get('bentity_id').upper())
    
    # lat and lon
    if request.GET.get('lat') and request.GET.get('lon'):
        filtered = True
        records = records.filter(lat=request.GET.get('lat'), lon=request.GET.get('lon'))
    
    
    # status
    if request.GET.get('status'):
        records = records.filter(status=request.GET.get('status')[0].upper())
        
        
    # error message if the user didn't supply an argument to filter the records
    if not filtered: 
        return errorResponse("Please supply at least one these argument-combinations: 'gabi_acc_number', ('species' and 'bentity_id'), or ('lat' and 'lon').", format, {'records': []})
         
    
    # fetch all the bentitites at once, so we don't have to hit the database once for each record
    records = records.prefetch_related('bentity') 
        
    output_objects = [{
            'gabi_acc_number': r.gabi_acc_number,
            'species': r.valid_species_name_id,
            'bentity_id': r.bentity_id,
            'bentity_name': r.bentity.bentity,
            'status': r.status,
            'type_of_data': r.type_of_data,
            'lat': r.lat,
            'lon': r.lon,  
            'citation': r.citation,
        } for r in records]
    
    
    
    if format == 'csv':
        return CSVResponse(output_objects, ('gabi_acc_number', 'species', 'bentity_id', 'bentity_name', 'lat', 'lon', 'status', 'type_of_data', 'citation'))
    
    else:
        return JSONResponse({'records': output_objects})
    
    
    
    
    
        
        
def species_range(request, format='json'):
    """
    Given a 'species' in the URL query string, return a JSON or CSV response with a
    list of bentities for which that species has a record, along 
    with the category code for each.
    
    Outputted JSON is a list with {gid:xxx, category:xxx} for each bentity where
    the species has a record.
    
    If the bentity does not have any records for the specified species, there 
    will not be an object for the bentity in the results.
    
    """

    species = request.GET.get('species')
    
    if species:
        # look up category for this species for each bentity from the database        
        bentities = ( SpeciesBentityPair.objects
                     .filter(valid_species_name=species.capitalize())
                     .only('bentity', 'category','num_records','literature_count','museum_count','database_count') )
    
   
    else: # punt if the request doesn't have a species
       return errorResponse("Please supply a 'species' argument.", format, {'records': []})
    
    
    if format == 'csv':
        # return CSV
        return CSVResponse(
            [{
                'species': species,
                'bentity_id': b.bentity_id,
                'bentity_name': b.bentity.bentity,
                'status': b.category,
                'num_records': b.num_records,
                'literature_count': b.literature_count,
                'museum_count': b.museum_count,
                'database_count': b.database_count,
                 
            } for b in bentities],
            fields=('species', 'bentity_id', 'bentity_name', 'status', 'num_records', 'literature_count', 'museum_count', 'database_count')  )
    
    else:
        # serialize to JSON    
        json_objects = [{'gid': b.bentity_id, 'category': b.category, 'num_records':b.num_records, 'literature_count':b.literature_count, 
        'museum_count':b.museum_count, 'database_count':b.database_count} for b in bentities]
        
        return JSONResponse({'bentities': json_objects})
    
   
        
        
        
        

def species_per_bentity(request, format='json'):
    """
    Return a JSON response with a list of bentities, the number of native
    species in each bentity, the number of records found in each bentity, 
    and out of the total records what number are museum records, database records,
    and literature records.  Filter by "genus_name" or "subfamily_name" arguments
    if present in the URL query string.  If both are presetnt, only "genus_name"
    will be used.
    
    This view will query the "map_species_bentity_pair" view if "genus_name" or 
    "subfamily_name" is supplied in the query string, and will query the 
    "map_bentity_count" view if neither is supplied.
    
    Outputted JSON is a list with {gid:xxx, species_count:xxx, num_records:xxx, 
    literature_count:xxx, museum_count:xxx, database_count:xxx} for each bentity.
    
    If the bentity does not have any species matching the query, there will not
    be an object for the bentity in the results.
    """
    
    bentities = []
    
    genus = request.GET.get('genus')
    subfamily = request.GET.get('subfamily')
    
    if genus: # use genus name
        bentities = Bentity.objects.raw("""
            SELECT "bentity2_id" AS "bentity2_id", count(distinct "valid_species_name") AS "species_count",
            		sum("literature_count"::int) AS "literature_count", 
            		sum("museum_count"::int) AS "museum_count",
            		sum("database_count"::int) AS "database_count",
            		sum("num_records"::int) AS "num_records"
            FROM "map_species_bentity_pair"
            WHERE "genus_name" = %s
            AND "category" = 'N'
            GROUP BY "bentity2_id"     
            """, [genus.capitalize()]) 
        
        
    elif subfamily: # use subfamily name
        bentities = Bentity.objects.raw("""
            SELECT "bentity2_id" AS "bentity2_id", count(distinct "valid_species_name") AS "species_count",
            		sum("literature_count"::int) AS "literature_count", 
            		sum("museum_count"::int) AS "museum_count",
            		sum("database_count"::int) AS "database_count",
            		sum("num_records"::int) AS "num_records"
            FROM "map_species_bentity_pair"
            WHERE "subfamily_name" = %s
            AND "category" = 'N'
            GROUP BY "bentity2_id"  
            """, [subfamily.capitalize()]) 
    
    else: # no filter supplied, return total species richness
        bentities = Bentity.objects.raw("""
            SELECT "bentity2_id", "species_count", "literature_count"::int, "museum_count"::int, "database_count"::int, "num_records"::int 
            FROM "map_bentity_count";
        """)
        
    
    
    
    if format == 'csv':
        return CSVResponse(
            [{
                'bentity_id': b.gid,
                'bentity_name': b.bentity,
                'species_count': b.species_count,
                'num_records': b.num_records,
                'literature_count': b.literature_count, 
                'museum_count': b.museum_count,
                'database_count': b.database_count
            } for b in bentities],
            fields=('bentity_id', 'bentity_name', 'species_count', 'num_records', 'literature_count', 'museum_count', 'database_count')   )
    
    
    else:  
        # serialize to JSON    
        json_objects = [{'gid': b.gid, 'species_count': b.species_count, 'num_records':b.num_records,
        'literature_count':b.literature_count, 'museum_count': b.museum_count,'database_count':b.database_count} for b in bentities]
        return JSONResponse({'bentities': json_objects})
    
    
    
    
    
    
def species_in_common(request, format='json'):
    """
    Given a 'bentity' in the URL query string, return a JSON response with a list
    of bentities, a count of how many native species each other bentity has 
    in common with the given bentity, the number of records that are found in other 
    bentities that share species with the selected bentity, and out of the total records 
    what number are museum records, database records, and literature records.
    
    For each bentity, include {gid:xxx, species_count:xxx, num_records:xxx, 
    literature_count:xxx, museum_count:xxx, database_count:xxx}
    
    If the bentity does not have any species matching the query, there will not
    be an object for the bentity in the results.
    """
    
    query_bentity_id = request.GET.get('bentity_id')
    
    if query_bentity_id:
        bentities = Bentity.objects.raw("""
            SELECT r2."bentity2_id" AS "bentity2_id", 
                count(distinct r2."valid_species_name") AS "species_count"
            FROM "map_species_bentity_pair" AS r1
            INNER JOIN "map_species_bentity_pair" AS r2
            ON r1."valid_species_name" = r2."valid_species_name"
            WHERE r1."bentity2_id" = %s
            AND r1."category" = 'N'
            AND r2."category" = 'N'
            GROUP BY r2."bentity2_id";
            """, [query_bentity_id])
    
    
    else:
        return errorResponse("Please supply a 'bentity_id' argument.", format, {'bentities':[]})
      
      
      
      
    if format == 'csv':
        return CSVResponse(
            [{
                'query_bentity_id': query_bentity_id,
                'bentity_id': b.gid,
                'bentity_name': b.bentity,
                'species_in_common': b.species_count
            } for b in bentities],
            fields=('query_bentity_id', 'bentity_id', 'bentity_name', 'species_in_common')   )
        
    else:  
        # serialize to JSON
        json_objects = [{
            'gid': b.gid, 
            'species_count': b.species_count
            } for b in bentities]
        return JSONResponse({'bentities': json_objects})
        
        
        
