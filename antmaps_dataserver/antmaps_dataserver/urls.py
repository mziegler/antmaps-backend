"""
URL Routing
(Maps URL of incoming request to Python function)
"""

from django.conf.urls import patterns, include, url

#import bentities.views
import queries.views

urlpatterns = [
    # Examples:
    # url(r'^$', 'antmaps_dataserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    
    
    # for populating taxon select boxes
    url(r'^subfamily-list', queries.views.subfamily_list),
    url(r'^genus-list', queries.views.genus_list),
    url(r'^species-list', queries.views.species_list),
    
    # get points for a species to plot on map
    url(r'^species-points', queries.views.species_points),
    
    # for genus and subfamily diversity modes
    url(r'^species-per-bentity', queries.views.species_per_bentity),
    
    # for bentity diversity mode
    url(r'^species-in-common', queries.views.species_in_common),
]
