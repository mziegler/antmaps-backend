"""
URL Routing
(Maps URL of incoming request to Python function)
"""

from django.conf.urls import include, url


import queries.views
import error_report.views


# regular expression to capture the file extension as CSV or JSON
f = r'\.?(?P<format>csv|json)?' 


urlpatterns = [
    # Examples:
    # url(r'^$', 'antmaps_dataserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    
    
    
    ####################################################################
    # Public API
    

    # for species mode categories
    url(r'^species-bentity-categories'+f, queries.views.species_range), # deprecating
    url(r'^species-range'+f, queries.views.species_range),
    
    # for genus and subfamily diversity modes
    url(r'^species-per-bentity'+f, queries.views.species_per_bentity), # deprecating
    url(r'^bentity-species-counts'+f, queries.views.species_per_bentity),
    
    # for bentity diversity mode
    url(r'^species-in-common'+f, queries.views.species_in_common),
    
    
    # species autocomplete
    url(r'^species-autocomplete'+f, queries.views.species_autocomplete), # deprecating
    url(r'^species-search'+f, queries.views.species_autocomplete),
    
    # get points for a species to plot on map
    url(r'^species-points'+f, queries.views.species_points), 
    
    #get metadata for a species for a bentity
    url(r'^species-metadata'+f,queries.views.species_metadata),

    
    
    # for populating taxon select boxes (OLD - to be deprecated)
    url(r'^subfamily-list'+f, queries.views.subfamily_list),
    url(r'^genus-list'+f, queries.views.genus_list),
    url(r'^species-list'+f, queries.views.species_list),
    url(r'^bentity-list'+f, queries.views.bentity_list),
    
    # new URL's for public API
    url(r'^subfamilies'+f, queries.views.subfamily_list),
    url(r'^genera'+f, queries.views.genus_list),
    url(r'^species'+f, queries.views.species_list), # must be after the other URLs starting with 'species'
    url(r'^bentities'+f, queries.views.bentity_list),
    
    
    
    
    #########################################################################
    # Not part of public API (used by antmaps.org front-end only)
    
    # for antweb and antwiki links. for diversity and species modes
    url(r'^antweb-links', queries.views.antweb_links),
    
    # report data error
    url(r'^error-report', error_report.views.report),
    
 
]
