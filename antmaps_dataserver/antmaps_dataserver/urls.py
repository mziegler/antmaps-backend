from django.conf.urls import patterns, include, url

#import bentities.views
import speciesmode.views

urlpatterns = [
    # Examples:
    # url(r'^$', 'antmaps_dataserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    
    #url(r'^bentities', bentities.views.bentity_polygons),
    
    # for populating taxon select boxes
    url(r'^subfamily-list', speciesmode.views.subfamily_list),
    url(r'^genus-list', speciesmode.views.genus_list),
    url(r'^species-list', speciesmode.views.species_list),
    
    # get points for a species to plot on map
    url(r'^species-points', speciesmode.views.species_points),
    
    # for genus and subfamily diversity modes
    url(r'^species-per-bentity', speciesmode.views.species_per_bentity),
    
    # for bentity diversity mode
    url(r'^species-in-common', speciesmode.views.species_in_common),
]
