from common import *

DEBUG = False

# enable asset compression on production
# it defaults to the opposite of debug
COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter',  'compressor.filters.cssmin.CSSMinFilter']

COMPRESS_OFFLINE = True
COMPRESS_OUTPUT_DIR = 'prod'

# Django Bakery
BUILD_DIR = os.path.join(BASE_DIR, 'build')
BAKERY_VIEWS = (
    # Django Bakery Views go here
    # '{{ project_name }}.apps.some_news_app.views.SomeNewsAppView',
)
AWS_STAGING_BUCKET_NAME = ''
AWS_BUCKET_NAME = 'apps-cironline-org'

# Defaults to project name. Add correct one
#ALLOWED_HOSTS = ['apps.cironline.org']

# Static
STATIC_URL = '//s3-us-west-1.amazonaws.com/media-apps-cironline-org/{{ project_name }}/'
