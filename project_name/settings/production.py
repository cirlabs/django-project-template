from common import *

DEBUG = False

HEROKU_DEPLOY = False

# enable asset compression on production
# it defaults to the opposite of debug
COMPRESS_ENABLED = True

# Defaults to project name. Add correct one
ALLOWED_HOSTS = ['{{ project_name }}.apps.cironline.org']

if DEBUG:
    MIDDLEWARE_CLASSES.append('apps.core.middleware.LoginRequiredMiddleware')

# Databases
if HEROKU_DEPLOY:
    import dj_database_url # Heroku only
    # Heroku Specific
    DATABASES['default'] =  dj_database_url.config()

    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
else:
    # Production database info
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': '{{ project_name }}',
            'PORT': '6432',  # PGBouncer port
            'HOST': 'ec2-54-244-141-139.us-west-2.compute.amazonaws.com',
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