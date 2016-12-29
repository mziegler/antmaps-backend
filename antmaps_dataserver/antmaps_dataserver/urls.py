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
    
    
    # for populating taxon select boxes
    url(r'^subfamily-list'+f, queries.views.subfamily_list),
    url(r'^genus-list'+f, queries.views.genus_list),
    url(r'^species-list'+f, queries.views.species_list),
    url(r'^bentity-list'+f, queries.views.bentity_list),
    
    # species autocomplete
    url(r'^species-autocomplete'+f, queries.views.species_autocomplete),
    
    # get points for a species to plot on map
    url(r'^species-points'+f, queries.views.species_points),
    
    #get metadata for a species for a bentity
    url(r'^species-metadata'+f,queries.views.species_metadata),
    
    # for species mode categories
    url(r'^species-bentity-categories'+f, queries.views.species_bentities_categories),
    
    # for genus and subfamily diversity modes
    url(r'^species-per-bentity'+f, queries.views.species_per_bentity),
    
    # for bentity diversity mode
    url(r'^species-in-common'+f, queries.views.species_in_common),
    
    # for antweb and antwiki links. for diversity and species modes
    url(r'^antweb-links'+f, queries.views.antweb_links),
    
    # report data error
    url(r'^error-report'+f, error_report.views.report),
    
 
]
