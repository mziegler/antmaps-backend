"""
URL Routing
(Maps URL of incoming request to Python function)
"""

from django.conf.urls import include, url


import queries.views
import error_report.views

urlpatterns = [
    # Examples:
    # url(r'^$', 'antmaps_dataserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    
    
    # for populating taxon select boxes
    url(r'^subfamily-list', queries.views.subfamily_list),
    url(r'^genus-list', queries.views.genus_list),
    url(r'^species-list', queries.views.species_list),
    url(r'^bentity-list', queries.views.bentity_list),
    
    # species autocomplete
    url(r'^species-autocomplete', queries.views.species_autocomplete),
    
    # get points for a species to plot on map
    url(r'^species-points', queries.views.species_points),
    
    #get metadata for a species for a bentity
    url(r'^species-metadata',queries.views.species_metadata),
    
    # for species mode categories
    url(r'^species-bentity-categories', queries.views.species_bentities_categories),
    
    # for genus and subfamily diversity modes
    url(r'^species-per-bentity', queries.views.species_per_bentity),
    
    # for bentity diversity mode
    url(r'^species-in-common', queries.views.species_in_common),
    
    # for antweb and antwiki links. for diversity and species modes
    url(r'^antweb-links', queries.views.antweb_links),
    
    # report data error
    url(r'^error-report', error_report.views.report),
    
 
]
