"""
Django settings for antmaps_dataserver project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/


# WARNING!
# This (not-so) secret key is currently publicly available on Github.  That's okay
# for now, because this app doesn't need to do anything secure, but if that changes,
# (eg. we start having authentication and user accounts,) make sure to change the
# secret key and keep the new key out of Github (put in a separate file).

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4$+@f2c752oqe1fiivax_arjr9awpd(*t1)0&25c#3p!b3j#_n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('ANTMAPS_DEBUG') or False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['.antmaps.unit.oist.jp','.antmaps.org','.localhost']


# Application definition

# Uncomment some of these back on if the antmaps website ever needs to be secure
# (if user accounts are ever implemented.)

INSTALLED_APPS = (
    #'django.contrib.gis',
    #'django.contrib.admin',
    #'django.contrib.auth',
    #'django.contrib.contenttypes',
    #'django.contrib.sessions',
    #'django.contrib.messages',
    #'django.contrib.staticfiles',
    'queries',
    'error_report',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware', # must be first
    #'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware', # security-related
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware', # security-related
    'django.middleware.cache.FetchFromCacheMiddleware', # must be last
)







# If in debug mode, use a special URLconf that 1) serves static files, and 2)
# prepends a "dataserver/" to Django URL views.  In production, we should do this
# with Apache.
if DEBUG:
    ROOT_URLCONF = 'antmaps_dataserver.urls_debug'
else:
    ROOT_URLCONF = 'antmaps_dataserver.urls'


WSGI_APPLICATION = 'antmaps_dataserver.wsgi.application'






# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        
        # get connection parameters from environment variables
        'NAME': os.environ.get('ANTMAPS_DB_NAME'),
        'HOST': os.environ.get('ANTMAPS_DB_HOST'),
        'PORT': os.environ.get('ANTMAPS_DB_PORT'),
        'USER': os.environ.get('ANTMAPS_DB_USER'),
        'PASSWORD': os.environ.get('ANTMAPS_DB_PASSWORD'),
        
        # for postgres connection optimization
        'timezone': 'UTC',
        'client_encoding': 'UTF8',
        'default_transaction_isolation': 'read committed',
        
    }
}







# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True





# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# serve static files from root URL (for in debug mode only)
STATIC_URL = '/'

# serve /antmaps-app as static files (debug mode only)
STATICFILES_DIRS = (os.path.join(BASE_DIR, '..', 'antmaps_frontend'),)





# Email connection parameters, for data error report
# Set from environment variables
EMAIL_HOST = os.environ.get('ANTMAPS_EMAIL_HOST')
EMAIL_PORT = os.environ.get('ANTMAPS_EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('ANTMAPS_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('ANTMAPS_EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.environ.get('ANTMAPS_EMAIL_USE_TLS') or False
EMAIL_USE_SSL = os.environ.get('ANTMAPS_EMAIL_USE_SSL') or False

# Where to send error report emails
REPORT_TO_EMAIL_ADDRESS = os.environ.get('ANTMAPS_REPORT_TO_EMAIL_ADDRESS')





TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            # ... some options here ...
        },
    },
]





# use memcached if the ANTMAPS_USE_MEMCACHED environment variable is set
# (otherwise fall back to Django's default in-memory cache)
if os.environ.get('ANTMAPS_USE_MEMCACHED'):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
            'LOCATION': '127.0.0.1:11211',
            'KEY_PREFIX': 'antmaps',
            
        }
    }
    CACHE_MIDDLEWARE_SECONDS = 60 * 60 * 4 # cache for 4 hours
