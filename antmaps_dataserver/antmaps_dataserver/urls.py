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
    url(r'^species-range'+f, queries.views.species_range),
    
    # for genus and subfamily diversity modes
    url(r'^species-per-bentity'+f, queries.views.species_per_bentity),
    
    # for bentity diversity mode
    url(r'^species-in-common'+f, queries.views.species_in_common),
    
    
    # species autocomplete
    url(r'^species-search'+f, queries.views.species_autocomplete),
    
    # bentity search
    url(r'^bentity-search'+f, queries.views.bentity_autocomplete),
    
    # get points for a species to plot on map
    url(r'^species-points'+f, queries.views.species_points), 

    # citations, for each species-location-paper occurrence
    url(r'^citations'+f, queries.views.citations),
    

    
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
