import os

from common import *

DEBUG = False

COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]

COMPRESS_OFFLINE = True
COMPRESS_OUTPUT_DIR = 'prod'

BUILD_DIR = os.path.join(BASE_DIR, 'build')
BAKERY_VIEWS = (
    # Django Bakery Views go here. Example:
    # '{{ project_name }}.apps.some_news_app.views.SomeNewsAppView',
)
AWS_STAGING_BUCKET_NAME = 'apps-staging-cironline-org'
AWS_BUCKET_NAME = 'apps-cironline-org'
AWS_MEDIA_BUCKET_NAME = 'media-apps-cironline-org'

VERBOSE_APP_NAME = None # App name in production. Defaults to project name

STATIC_URL = os.path.join(
    "//s3-us-west-1.amazonaws.com",
    AWS_MEDIA_BUCKET_NAME,
    VERBOSE_APP_NAME,
    '' # Adding an empty string ensures the path ends with a /
)
