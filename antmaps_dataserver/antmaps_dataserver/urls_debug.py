"""
This URLs.py is to be used in development mode only (not in production.)

The purpose of this file is to 
1) serve static files from the root URL, and
2) prepend the stem of "dataserver/" to all of the URLS in the django app.

In production, we should do both of these things using Apache (or other web server.)
"""


from django.conf.urls import include, url

# serve static files during development
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import redirect

urlpatterns = [
  # Examples:
  # url(r'^$', 'antmaps_dataserver.views.home', name='home'),
  # url(r'^blog/', include('blog.urls')),
  # url(r'^admin/', include(admin.site.urls)),
  
  # Route URLS prefixed by dataserver/ to main URL conf
  # (Let's deprecate /dataserver in favor of /api. )
  url(r'^dataserver/', include('antmaps_dataserver.urls')),
  url(r'^api/v01/', include('antmaps_dataserver.urls')),
  
  # redirect empty URL to index.html
  url(r'^$', lambda request: redirect('/index.html')),
  
] + staticfiles_urlpatterns() # serve static files in debug mode

