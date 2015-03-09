"""
This URLs.py is to be used in development mode only (not in production.)

The purpose of this file is to 
1) serve static files from the root URL, and
2) prepend the stem of "dataserver/" to all of the URLS in the django app.

In production, we should do both of these things using Apache (or other web server.)
"""


from django.conf.urls import patterns, include, url

# serve static files during development
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import redirect

urlpatterns = patterns('',
  # Examples:
  # url(r'^$', 'antmaps_dataserver.views.home', name='home'),
  # url(r'^blog/', include('blog.urls')),
  # url(r'^admin/', include(admin.site.urls)),
  
  # route URLS prefixed by dataserver/ to main URL conf
  url(r'^dataserver/', include('antmaps_dataserver.urls')),
  
  # redirect empty URL to index.html
  url(r'^$', lambda request: redirect('/index.html')),
  
) + staticfiles_urlpatterns()

