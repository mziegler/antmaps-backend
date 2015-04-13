"""
WSGI config for antmaps_dataserver project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "antmaps_dataserver.settings")

from django.core.wsgi import get_wsgi_application
_application = get_wsgi_application()

def application(environ, start_response):
    
    # Pass Apache environment variables starting with ANTMAPS_ to django via os.environ
    for key in environ:
        if key.startswith('ANTMAPS_'):
            os.environ[key] = environ[key]
            
    return _application(environ, start_response)
