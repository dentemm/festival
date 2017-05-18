from .base import *

from .config import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bql1e+0p5eaee42i_)(ohve%sm65&1na6$#vm$pgn&@tem$&gs'

DEBUG = True

try:
    from .local import *
except ImportError:
    pass

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()
	
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


#Dit werd voorlopig uitgeschakeld omdat Wagtail niet langer compressor out of the box ondersteunt

COMPRESS_ENABLED = True

COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_CSS_HASHING_METHOD = 'content'

# AMAZON S3 STORAGE
AWS_STORAGE_BUCKET_NAME = 'thinkmobile'
AWS_REGION = 'eu-central-1'
AWS_ACCESS_KEY_ID = 'AKIAJMC2L6WZ3TCR4RFQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_S3_HOST = 's3.eu-central-1.amazonaws.com'

AWS_S3_CUSTOM_DOMAIN = '%s.s3.eu-central-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'home.custom_storages.MediaStorage'
