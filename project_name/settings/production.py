from common import *

DEBUG = False

# enable asset compression on production
# it defaults to the opposite of debug
COMPRESS_ENABLED = True

# Defaults to project name. Add correct one
ALLOWED_HOSTS = ['{{ project_name }}.apps.cironline.org']

if DEBUG:
    MIDDLEWARE_CLASSES.append('apps.core.middleware.LoginRequiredMiddleware')

# Production database info
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '{{ project_name }}',
        'PORT': '6432',  # PGBouncer port
        'HOST': 'some-ec2-instance', # ec2-54-244-141-139.us-west-2.compute.amazonaws.com
        'USER': '{{ project_name }}',
        'PASSWORD': 'secret'
    }
}

# Static
STATIC_URL = 'http://media.apps.cironline.org/va_opiates_public/site_media/'

# GEOS paths for GeoDjango and GDAL. Configured for our particular Heroku setup.
GEOS_LIBRARY_PATH = '/app/.geodjango/geos/lib/libgeos_c.so'
GDAL_LIBRARY_PATH = '/app/.geodjango/gdal/lib/libgdal.so'

# Caching
CACHE_MIDDLEWARE_SECONDS = 90 * 60  # 90 minutes

os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';'),
        'TIMEOUT': 500,
        'BINARY': True,
    }
}