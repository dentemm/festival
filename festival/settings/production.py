from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bql1e+0p5eaee42i_)(ohve%sm65&1na6$#vm$pgn&@tem$&gs'

DEBUG = False

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